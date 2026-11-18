"""Orquestación reutilizable por creación y futura previsualización."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol

from saas_o_matic.domain.customers.value_objects import CountryCode
from saas_o_matic.domain.simulations.calculation import (
    Currency,
    ExchangeQuote,
    MonthlyCalculation,
    RateUnavailable,
    TaxCatalog,
    calculate_monthly,
)


class ExchangeRateProvider(Protocol):
    """Puerto de aplicación implementado estructuralmente sin imports hacia fuera."""

    def get_rate(self, currency: Currency) -> ExchangeQuote: ...


class MonthlyEstimator:
    def __init__(self, catalog: TaxCatalog, rates: ExchangeRateProvider) -> None:
        self._catalog = catalog
        self._rates = rates

    def estimate(
        self, subtotal: Decimal, country: CountryCode, currency: Currency
    ) -> MonthlyCalculation:
        rule = self._catalog.for_country(country)
        quote = (
            ExchangeQuote(Currency.EUR, Decimal("1"), None, datetime.now(UTC), "identity")
            if currency == Currency.EUR
            else self._rates.get_rate(currency)
        )
        if quote.currency != currency:
            raise RateUnavailable("La divisa recibida no coincide con la solicitada.")
        return calculate_monthly(subtotal, rule, quote)
