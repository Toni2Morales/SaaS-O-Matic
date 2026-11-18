"""Adaptador y caché con transporte/relojes falsos: suite sin Internet."""

from datetime import UTC, datetime
from decimal import Decimal
from email.message import Message
from unittest.mock import MagicMock
from urllib.error import HTTPError, URLError

import pytest

from saas_o_matic.domain.simulations.calculation import Currency, RateUnavailable
from saas_o_matic.infrastructure.frankfurter import FrankfurterRates, _request

NOW = datetime(2026, 11, 17, tzinfo=UTC)
VALID = b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1.080000000000000001}'


def test_eur_does_not_request() -> None:
    def forbidden(url: str, timeout: float) -> bytes:
        pytest.fail("EUR no debe consultar al proveedor")

    quote = FrankfurterRates(request=forbidden, now=lambda: NOW).get_rate(Currency.EUR)
    assert quote.rate == Decimal("1")
    assert quote.reference_date is None
    assert quote.source == "identity"


def test_cache_expiry_and_reference_date_are_independent() -> None:
    ticks = [0.0]
    calls: list[tuple[str, float]] = []

    def request(url: str, timeout: float) -> bytes:
        calls.append((url, timeout))
        return VALID

    rates = FrankfurterRates(request=request, clock=lambda: ticks[0], now=lambda: NOW)
    first = rates.get_rate(Currency.USD)
    assert first.rate == Decimal("1.080000000000000001")
    ticks[0] = 86399
    assert rates.get_rate(Currency.USD) is first
    assert len(calls) == 1
    ticks[0] = 86400
    assert rates.get_rate(Currency.USD) is not first
    assert calls == [("https://api.frankfurter.dev/v2/rate/EUR/USD", 5)] * 2


@pytest.mark.parametrize(
    ("currency", "rate", "expected"),
    [
        (Currency.USD, "1.08", "1.08"),
        (Currency.GBP, "0.85", "0.85"),
        (Currency.USD, "1.080000000000000001", "1.080000000000000001"),
        (Currency.USD, "1.1234567890123456789012345678901", "1.1234567890123456789012345678901"),
        (Currency.USD, "0.000001", "0.000001"),
        (Currency.USD, "1000000", "1000000"),
    ],
)
def test_legitimate_rates_and_boundaries_are_preserved(
    currency: Currency,
    rate: str,
    expected: str,
) -> None:
    body = (
        '{"date":"2026-11-16","base":"EUR","quote":"' + currency.value + '","rate":' + rate + "}"
    ).encode()

    def request(url: str, timeout: float) -> bytes:
        return body

    quote = FrankfurterRates(request=request, now=lambda: NOW).get_rate(currency)

    assert quote.rate == Decimal(expected)
    assert quote.rate.as_tuple() == Decimal(expected).as_tuple()


def test_invalid_extreme_rate_does_not_poison_cache_and_recovers() -> None:
    bodies = iter(
        [
            b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1e999999}',
            VALID,
            VALID,
        ]
    )
    calls = [0]

    def request(url: str, timeout: float) -> bytes:
        calls[0] += 1
        return next(bodies)

    provider = FrankfurterRates(request=request, now=lambda: NOW)

    with pytest.raises(RateUnavailable):
        provider.get_rate(Currency.USD)
    recovered = provider.get_rate(Currency.USD)
    assert recovered.rate == Decimal("1.080000000000000001")
    assert provider.get_rate(Currency.USD) is recovered
    assert calls[0] == 2


@pytest.mark.parametrize(
    "body",
    [
        b"not-json",
        b"[]",
        b"{}",
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1,"rate":2}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1e99999999999999999999999}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1e10000}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1e999999}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1e-10000}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":0.0000001}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1000000.1}',
        b'{"date":"2026-11-16","base":"EUR","quote":"USD","rate":1.12345678901234567890123456789012}',
        b'{"base":"USD","quote":"USD","rate":1,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"GBP","rate":1,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":0,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":-1,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":NaN,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":Infinity,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":true,"date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":"1.08","date":"2026-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":1,"date":"2026-02-30"}',
        b'{"base":"EUR","quote":"USD","rate":1,"date":"2027-11-16"}',
        b'{"base":"EUR","quote":"USD","rate":1,"date":"20261116"}',
    ],
)
def test_invalid_provider_payload_is_not_cached(body: bytes) -> None:
    calls = [0]

    def request(url: str, timeout: float) -> bytes:
        calls[0] += 1
        return body

    provider = FrankfurterRates(request=request, now=lambda: NOW)
    for _ in range(2):
        with pytest.raises(RateUnavailable):
            provider.get_rate(Currency.USD)
    assert calls[0] == 2


@pytest.mark.parametrize(
    "error",
    [
        TimeoutError(),
        URLError("offline"),
        HTTPError("https://api.frankfurter.dev", 503, "unavailable", Message(), None),
    ],
)
def test_external_failure_expired_not_served_and_recovery(error: Exception) -> None:
    ticks = [0.0]
    fail = [False]

    def request(url: str, timeout: float) -> bytes:
        if fail[0]:
            raise error
        return VALID

    provider = FrankfurterRates(request=request, clock=lambda: ticks[0], now=lambda: NOW)
    provider.get_rate(Currency.USD)
    fail[0] = True
    ticks[0] = 100
    assert provider.get_rate(Currency.USD).rate == Decimal("1.080000000000000001")
    ticks[0] = 86400
    fail[0] = True
    with pytest.raises(RateUnavailable):
        provider.get_rate(Currency.USD)
    fail[0] = False
    assert provider.get_rate(Currency.USD).rate == Decimal("1.080000000000000001")


def test_cache_keys_separate_currencies() -> None:
    calls = []

    def request(url: str, timeout: float) -> bytes:
        calls.append(url)
        return VALID.replace(b"USD", b"GBP") if url.endswith("GBP") else VALID

    provider = FrankfurterRates(request=request, now=lambda: NOW)
    assert provider.get_rate(Currency.USD).currency == Currency.USD
    assert provider.get_rate(Currency.GBP).currency == Currency.GBP
    assert len(calls) == 2


@pytest.mark.parametrize("status,size", [(503, 10), (200, 65537)])
def test_stdlib_transport_rejects_status_and_oversized_body(
    monkeypatch: pytest.MonkeyPatch,
    status: int,
    size: int,
) -> None:
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = status
    response.read.return_value = b"x" * size
    opener = MagicMock(return_value=response)
    monkeypatch.setattr("saas_o_matic.infrastructure.frankfurter.urlopen", opener)
    with pytest.raises(RateUnavailable):
        _request("https://api.frankfurter.dev/v2/rate/EUR/USD", 5)
    opener.assert_called_once_with("https://api.frankfurter.dev/v2/rate/EUR/USD", timeout=5)
    response.__exit__.assert_called_once()
