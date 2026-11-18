"""Servicio de cálculo del subtotal de usuarios."""

from __future__ import annotations

from decimal import Context, Decimal, localcontext

from saas_o_matic.domain.pricing.errors import InvalidUserCount
from saas_o_matic.domain.pricing.schedule import APPROVED_USER_PRICING_SCHEDULE


def _decimal_digits_upper_bound(value: int) -> int:
    """Devuelve una cota superior segura de los dígitos decimales de un entero.

    Para un entero positivo de ``b`` bits, ``b = 9q + r`` con ``0 <= r < 9``.
    Como ``2^9 < 10^3`` y ``2^r < 10^3``, se cumple
    ``value < 2^b < 10^(3q + 3)``. Por tanto, el entero tiene como máximo
    ``(b // 9 + 1) * 3`` dígitos decimales. La cota puede sobreestimar, pero
    evita convertir el entero completo a cadena y no usa coma flotante.
    """

    return (value.bit_length() // 9 + 1) * 3


def _validate_user_count(user_count: object) -> int:
    """Valida que la cantidad sea un entero no negativo, sin coerciones."""

    if isinstance(user_count, bool) or not isinstance(user_count, int) or user_count < 0:
        raise InvalidUserCount(user_count)
    return user_count


def calculate_user_subtotal(user_count: int) -> Decimal:
    """Calcula el subtotal de usuarios en EUR con los tramos aprobados.

    La función es pura: no conoce el plan, no persiste y no formatea el
    resultado. La precisión del contexto de ``Decimal`` se amplía en función
    de la cantidad para preservar la exactitud sin imponer un máximo.
    """

    validated_count = _validate_user_count(user_count)
    if validated_count == 0:
        return Decimal("0.00")
    schedule = APPROVED_USER_PRICING_SCHEDULE
    price_digits = max(len(band.price_per_user_eur.as_tuple().digits) for band in schedule.bands)
    digits_bound = _decimal_digits_upper_bound(validated_count)
    precision = max(28, digits_bound + price_digits + 10)

    with localcontext(Context(prec=precision)):
        total = Decimal(0)

        for band in schedule.bands:
            if validated_count < band.lower_bound:
                break

            upper_bound = band.upper_bound if band.upper_bound is not None else validated_count
            units = min(validated_count, upper_bound) - band.lower_bound + 1
            total += Decimal(units) * band.price_per_user_eur

        return total
