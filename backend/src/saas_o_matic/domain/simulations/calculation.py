"""Reglas puras y snapshots monetarios del presupuesto mensual."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from decimal import ROUND_HALF_UP, Context, Decimal, DecimalException, localcontext
from enum import StrEnum

from saas_o_matic.domain.customers.value_objects import CountryCode


class InvalidCalculation(ValueError):
    """Datos monetarios o catálogo incoherentes."""


class RateUnavailable(Exception):
    """El proveedor no puede suministrar una referencia válida."""


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"


# Límites técnicos de plausibilidad para una tasa externa, no límites comerciales.
# EUR/USD y EUR/GBP se mueven alrededor de 0,8-1,2; se dejan seis órdenes de
# magnitud de holgura y una precisión muy superior a la que publica el proveedor.
MIN_EXCHANGE_RATE = Decimal("0.000001")
MAX_EXCHANGE_RATE = Decimal("1000000")
MAX_EXCHANGE_RATE_DIGITS = 32


def validate_decimal(value: Decimal, *, positive: bool = False) -> None:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise InvalidCalculation("Se requiere un Decimal finito.")
    if value < 0 or (positive and value == 0):
        raise InvalidCalculation("Decimal fuera del rango admitido.")


def rounded_product(amount: Decimal, rate: Decimal) -> Decimal:
    """Multiplica exactamente antes del único redondeo comercial a céntimos."""

    validate_decimal(amount)
    validate_decimal(rate)
    precision = max(
        28,
        len(amount.as_tuple().digits) + len(rate.as_tuple().digits) + 4,
        amount.adjusted() + rate.adjusted() + 6,
    )
    try:
        with localcontext(Context(prec=precision, rounding=ROUND_HALF_UP)):
            result = (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except DecimalException as exc:
        raise InvalidCalculation("Importe no representable.") from exc
    validate_decimal(result)
    return result.copy_abs() if result == 0 else result


def validate_exchange_rate(rate: Decimal) -> None:
    """Rechaza tasas externas patológicas antes de cualquier cálculo o caché."""

    if rate < MIN_EXCHANGE_RATE or rate > MAX_EXCHANGE_RATE:
        raise InvalidCalculation("Tasa de cambio fuera del rango técnico admitido.")
    if len(rate.as_tuple().digits) > MAX_EXCHANGE_RATE_DIGITS:
        raise InvalidCalculation("Tasa de cambio con precisión no admitida.")


@dataclass(frozen=True, slots=True)
class TaxRule:
    country: CountryCode
    rate: Decimal
    source: str
    catalog_version: str
    verified_on: date
    territory: str
    effective_from: date | None = None

    def __post_init__(self) -> None:
        validate_decimal(self.rate)
        if self.rate > 1 or not self.source.startswith("https://"):
            raise InvalidCalculation("Regla fiscal inválida.")
        if not self.catalog_version or not self.territory:
            raise InvalidCalculation("Faltan metadatos fiscales.")


class TaxCatalog:
    """Catálogo inmutable sin tasa por defecto ni países faltantes/duplicados."""

    def __init__(self, rules: tuple[TaxRule, ...]) -> None:
        if len(rules) != len(CountryCode) or {r.country for r in rules} != set(CountryCode):
            raise InvalidCalculation("El catálogo debe cubrir exactamente los países admitidos.")
        self._rules = {r.country: r for r in rules}

    def for_country(self, country: CountryCode) -> TaxRule:
        try:
            return self._rules[country]
        except KeyError as exc:
            raise InvalidCalculation("País sin configuración fiscal.") from exc


@dataclass(frozen=True, slots=True)
class ExchangeQuote:
    currency: Currency
    rate: Decimal
    reference_date: date | None
    obtained_at: datetime
    source: str

    def __post_init__(self) -> None:
        validate_decimal(self.rate, positive=True)
        validate_exchange_rate(self.rate)
        if self.obtained_at.utcoffset() is None:
            raise InvalidCalculation("La fecha de obtención debe incluir zona horaria.")
        if self.currency == Currency.EUR:
            if self.rate != 1 or self.reference_date is not None or self.source != "identity":
                raise InvalidCalculation("Conversión identidad incoherente.")
        elif (
            self.source != "frankfurter"
            or self.reference_date is None
            or self.reference_date > self.obtained_at.astimezone(UTC).date()
        ):
            raise InvalidCalculation("Referencia externa incoherente.")


@dataclass(frozen=True, slots=True)
class MonthlyCalculation:
    tax_country: str
    tax_rate: Decimal
    tax_source: str
    tax_catalog_version: str
    tax_verified_on: date
    tax_territory: str
    tax_effective_from: date | None
    tax_amount_eur: Decimal
    total_eur: Decimal
    display_currency: str
    exchange_rate: Decimal
    exchange_rate_date: date | None
    exchange_rate_obtained_at: datetime
    exchange_rate_source: str
    converted_total: Decimal

    def validate_against(self, subtotal: Decimal) -> None:
        """Valida también snapshots recuperados sin consultar catálogos actuales."""

        for amount in (subtotal, self.tax_amount_eur, self.total_eur, self.converted_total):
            validate_decimal(amount)

        TaxRule(
            CountryCode(self.tax_country),
            self.tax_rate,
            self.tax_source,
            self.tax_catalog_version,
            self.tax_verified_on,
            self.tax_territory,
            self.tax_effective_from,
        )
        ExchangeQuote(
            Currency(self.display_currency),
            self.exchange_rate,
            self.exchange_rate_date,
            self.exchange_rate_obtained_at,
            self.exchange_rate_source,
        )
        if self.tax_amount_eur != rounded_product(subtotal, self.tax_rate):
            raise InvalidCalculation("Snapshot fiscal inconsistente.")
        with localcontext(Context(prec=max(28, subtotal.adjusted() + 8))):
            if self.total_eur != subtotal + self.tax_amount_eur:
                raise InvalidCalculation("Total histórico inconsistente.")
        if self.converted_total != rounded_product(self.total_eur, self.exchange_rate):
            raise InvalidCalculation("Conversión histórica inconsistente.")

    def snapshot(self) -> dict[str, str | None]:
        """Dinero y tasas serializados como cadenas, nunca números JSON."""

        result: dict[str, str | None] = {"schema_version": "1"}
        money = {"tax_amount_eur", "total_eur", "converted_total"}
        for key, value in asdict(self).items():
            if isinstance(value, Decimal):
                result[key] = format(value, ".2f" if key in money else "f")
            elif isinstance(value, date):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    @classmethod
    def restore(cls, values: dict[str, str | None]) -> MonthlyCalculation:
        """Reconstruye el snapshot versionado; la entidad valida sus fórmulas."""

        def required(key: str) -> str:
            value = values[key]
            if not isinstance(value, str):
                raise InvalidCalculation("Snapshot incompleto.")
            return value

        def optional_date(key: str) -> date | None:
            return date.fromisoformat(required(key)) if values[key] is not None else None

        if required("schema_version") != "1":
            raise InvalidCalculation("Versión de snapshot desconocida.")
        return cls(
            tax_country=required("tax_country"),
            tax_rate=Decimal(required("tax_rate")),
            tax_source=required("tax_source"),
            tax_catalog_version=required("tax_catalog_version"),
            tax_verified_on=date.fromisoformat(required("tax_verified_on")),
            tax_territory=required("tax_territory"),
            tax_effective_from=optional_date("tax_effective_from"),
            tax_amount_eur=Decimal(required("tax_amount_eur")),
            total_eur=Decimal(required("total_eur")),
            display_currency=required("display_currency"),
            exchange_rate=Decimal(required("exchange_rate")),
            exchange_rate_date=optional_date("exchange_rate_date"),
            exchange_rate_obtained_at=datetime.fromisoformat(required("exchange_rate_obtained_at")),
            exchange_rate_source=required("exchange_rate_source"),
            converted_total=Decimal(required("converted_total")),
        )


def calculate_monthly(subtotal: Decimal, rule: TaxRule, quote: ExchangeQuote) -> MonthlyCalculation:
    tax = rounded_product(subtotal, rule.rate)
    with localcontext(Context(prec=max(28, subtotal.adjusted() + 8))):
        total = subtotal + tax
    result = MonthlyCalculation(
        rule.country.value,
        rule.rate,
        rule.source,
        rule.catalog_version,
        rule.verified_on,
        rule.territory,
        rule.effective_from,
        tax,
        total,
        quote.currency.value,
        quote.rate,
        quote.reference_date,
        quote.obtained_at,
        quote.source,
        rounded_product(total, quote.rate),
    )
    result.validate_against(subtotal)
    return result
