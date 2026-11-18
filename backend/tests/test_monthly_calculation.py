"""Impuestos oficiales, redondeo y aislamiento monetario sin I/O."""

from dataclasses import FrozenInstanceError, replace
from datetime import UTC, date, datetime
from decimal import Decimal, localcontext
from typing import Any, cast

import pytest

from saas_o_matic.domain.customers.value_objects import CountryCode
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
from saas_o_matic.domain.simulations.calculation import (
    Currency,
    ExchangeQuote,
    InvalidCalculation,
    TaxCatalog,
    calculate_monthly,
    rounded_product,
)
from saas_o_matic.domain.simulations.entities import format_eur_amount
from saas_o_matic.infrastructure.tax_catalog import configured_tax_catalog


def _quote(currency: Currency = Currency.EUR, rate: str = "1") -> ExchangeQuote:
    return ExchangeQuote(
        currency,
        Decimal(rate),
        None if currency == Currency.EUR else date(2026, 11, 16),
        datetime(2026, 11, 17, tzinfo=UTC),
        "identity" if currency == Currency.EUR else "frankfurter",
    )


@pytest.mark.parametrize(
    "country,tax,total",
    [
        ("ES", "29.40", "169.40"),
        ("PT", "32.20", "172.20"),
        ("FR", "28.00", "168.00"),
        ("DE", "26.60", "166.60"),
        ("IT", "30.80", "170.80"),
        ("NL", "29.40", "169.40"),
    ],
)
def test_verified_country_examples(country: str, tax: str, total: str) -> None:
    rule = configured_tax_catalog().for_country(CountryCode(country))
    result = calculate_monthly(calculate_user_subtotal(15), rule, _quote())
    assert result.tax_amount_eur == Decimal(tax)
    assert result.total_eur == Decimal(total)
    assert result.converted_total == result.total_eur
    assert result.tax_source == rule.source
    assert result.tax_effective_from is None


@pytest.mark.parametrize(
    "users,tax,total",
    [
        (0, "0.00", "0.00"),
        (1, "2.10", "12.10"),
        (10, "21.00", "121.00"),
        (11, "22.68", "130.68"),
        (50, "88.20", "508.20"),
        (51, "89.25", "514.25"),
        (100, "140.70", "810.70"),
        (1000000, "1050035.70", "6050205.70"),
    ],
)
def test_spanish_pricing_boundaries(users: int, tax: str, total: str) -> None:
    result = calculate_monthly(
        calculate_user_subtotal(users),
        configured_tax_catalog().for_country(CountryCode.ES),
        _quote(),
    )
    assert result.tax_amount_eur.as_tuple() == Decimal(tax).as_tuple()
    assert result.total_eur.as_tuple() == Decimal(total).as_tuple()


@pytest.mark.parametrize(
    "amount,rate,expected",
    [
        ("0.05", "0.10", "0.01"),
        ("0.01", "0.49", "0.00"),
        ("0.01", "0.50", "0.01"),
        ("169.40", "1.08", "182.95"),
    ],
)
def test_half_up(amount: str, rate: str, expected: str) -> None:
    assert (
        rounded_product(Decimal(amount), Decimal(rate)).as_tuple() == Decimal(expected).as_tuple()
    )


@pytest.mark.parametrize("rate", ["-1", "NaN", "Infinity", "sNaN"])
def test_invalid_tax_rate(rate: str) -> None:
    with pytest.raises(InvalidCalculation):
        replace(configured_tax_catalog().for_country(CountryCode.ES), rate=Decimal(rate))


def test_catalog_rejects_missing_duplicate_country_and_no_default() -> None:
    catalog = configured_tax_catalog()
    rules = tuple(catalog.for_country(c) for c in CountryCode)
    with pytest.raises(InvalidCalculation):
        TaxCatalog(rules[:-1])
    with pytest.raises(InvalidCalculation):
        TaxCatalog((*rules[:-1], rules[0]))
    with pytest.raises(InvalidCalculation):
        catalog.for_country(cast(Any, "US"))


def test_monetry_context_is_independent_and_snapshot_immutable() -> None:
    rule = configured_tax_catalog().for_country(CountryCode.ES)
    quote = _quote(Currency.USD, "1.080000000000000000001")
    with localcontext() as context:
        context.prec = 2
        context.Emax = 2
        for signal in context.traps:
            context.traps[signal] = True
        before = (context.prec, context.Emax, dict(context.traps), dict(context.flags))
        subtotal = calculate_user_subtotal(1000)
        result = calculate_monthly(subtotal, rule, quote)
        assert subtotal == Decimal("5170.00")
        assert format_eur_amount(subtotal) == "5170.00"
        assert result.exchange_rate.as_tuple() == quote.rate.as_tuple()
        assert (context.prec, context.Emax, dict(context.traps), dict(context.flags)) == before
    with pytest.raises(FrozenInstanceError):
        cast(Any, result).tax_rate = Decimal("0.99")
    assert result.tax_rate == Decimal("0.21")
    changed = replace(rule, rate=Decimal("0.99"), catalog_version="changed-test")
    later = calculate_monthly(subtotal, changed, quote)
    assert later.tax_amount_eur != result.tax_amount_eur
    assert type(result).restore(result.snapshot()) == result


@pytest.mark.parametrize("currency", [Currency.USD, Currency.GBP])
def test_foreign_conversion(currency: Currency) -> None:
    result = calculate_monthly(
        Decimal("140.00"),
        configured_tax_catalog().for_country(CountryCode.ES),
        _quote(currency, "1.08"),
    )
    assert result.converted_total == Decimal("182.95")


@pytest.mark.parametrize(
    "rate",
    [
        "0.000001",
        "1000000",
        "1.1234567890123456789012345678901",
    ],
)
def test_exchange_rate_technical_bounds_are_calculable(rate: str) -> None:
    result = calculate_monthly(
        Decimal("140.00"),
        configured_tax_catalog().for_country(CountryCode.ES),
        _quote(Currency.USD, rate),
    )

    assert result.exchange_rate == Decimal(rate)
    assert result.converted_total >= 0


@pytest.mark.parametrize(
    "rate",
    [
        "0",
        "-1",
        "NaN",
        "Infinity",
        "0.0000001",
        "1000000.1",
        "1e10000",
        "1e-10000",
        "1.12345678901234567890123456789012",
    ],
)
def test_exchange_quote_rejects_pathological_rates(rate: str) -> None:
    with pytest.raises(InvalidCalculation):
        _quote(Currency.USD, rate)
