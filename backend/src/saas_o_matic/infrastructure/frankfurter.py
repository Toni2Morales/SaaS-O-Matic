"""Único adaptador externo, JSON Decimal y caché en memoria por proceso."""

import json
import re
from collections.abc import Callable
from datetime import UTC, date, datetime
from decimal import Decimal, DecimalException
from threading import Lock
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from saas_o_matic.domain.simulations.calculation import (
    Currency,
    ExchangeQuote,
    InvalidCalculation,
    RateUnavailable,
)


def _request(url: str, timeout: float) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        if response.status != 200:
            raise RateUnavailable("Respuesta externa no satisfactoria.")
        body: bytes = response.read(65537)
        if len(body) > 65536:
            raise RateUnavailable("Respuesta externa demasiado grande.")
        return body


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Campo duplicado en la respuesta externa.")
        result[key] = value
    return result


class FrankfurterRates:
    TTL_SECONDS = 86400
    TIMEOUT_SECONDS = 5

    def __init__(
        self,
        request: Callable[[str, float], bytes] = _request,
        clock: Callable[[], float] = monotonic,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._request = request
        self._clock = clock
        self._now = now
        self._cache: dict[Currency, tuple[float, ExchangeQuote]] = {}
        self._lock = Lock()

    def get_rate(self, currency: Currency) -> ExchangeQuote:
        if currency == Currency.EUR:
            return ExchangeQuote(currency, Decimal("1"), None, self._now(), "identity")
        with self._lock:
            cached = self._cache.get(currency)
            if cached is not None and self._clock() < cached[0]:
                return cached[1]
            try:
                body = self._request(
                    f"https://api.frankfurter.dev/v2/rate/EUR/{currency.value}",
                    self.TIMEOUT_SECONDS,
                )
                payload = json.loads(
                    body,
                    parse_float=Decimal,
                    parse_int=Decimal,
                    parse_constant=Decimal,
                    object_pairs_hook=_unique_object,
                )
                if not isinstance(payload, dict):
                    raise ValueError("Objeto externo requerido.")
                if payload.get("base") != "EUR" or payload.get("quote") != currency.value:
                    raise ValueError("Par de divisas incoherente.")
                rate = payload["rate"]
                reference = payload["date"]
                if not isinstance(rate, Decimal) or not isinstance(reference, str):
                    raise ValueError("Tipos externos incoherentes.")
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", reference) is None:
                    raise ValueError("Fecha externa inválida.")
                quote = ExchangeQuote(
                    currency, rate, date.fromisoformat(reference), self._now(), "frankfurter"
                )
            except HTTPError as exc:
                exc.close()
                raise RateUnavailable("El proveedor devolvió un error HTTP.") from exc
            except (
                URLError,
                OSError,
                TimeoutError,
                ValueError,
                KeyError,
                InvalidCalculation,
                DecimalException,
                RecursionError,
            ) as exc:
                raise RateUnavailable("No hay un tipo de cambio válido disponible.") from exc
            self._cache[currency] = (self._clock() + self.TTL_SECONDS, quote)
            return quote
