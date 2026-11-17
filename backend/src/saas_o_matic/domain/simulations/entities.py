"""Entidades y utilidades monetarias del dominio de simulaciones."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, localcontext
from uuid import UUID

_CENT = Decimal("0.01")


class SimulationDomainError(ValueError):
    """Error base del dominio de simulaciones."""


class InvalidSimulationUserCount(SimulationDomainError):
    """El número de usuarios no es un entero positivo."""

    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__("El número de usuarios debe ser un entero positivo.")


class InvalidSimulationAmount(SimulationDomainError):
    """El importe no es un Decimal exacto representable con dos decimales."""


def format_eur_amount(value: Decimal) -> str:
    """Devuelve un importe EUR como texto decimal canónico con dos decimales.

    La función no redondea: si el valor requiere más precisión de la soportada
    por el alcance actual, se rechaza explícitamente.
    """

    if not isinstance(value, Decimal):
        raise InvalidSimulationAmount("El importe debe ser un Decimal.")
    if not value.is_finite() or value < 0:
        raise InvalidSimulationAmount("El importe debe ser un Decimal finito y no negativo.")

    try:
        with localcontext() as context:
            context.prec = max(28, len(value.as_tuple().digits) + 2)
            quantized = value.quantize(_CENT)
    except InvalidOperation as exc:
        raise InvalidSimulationAmount(
            "El importe no se puede representar con dos decimales."
        ) from exc

    if quantized != value:
        raise InvalidSimulationAmount("El importe tiene más de dos decimales.")
    if quantized == 0:
        quantized = abs(quantized)

    return format(quantized, "f")


@dataclass(frozen=True, slots=True)
class Simulation:
    """Simulación persistida con el subtotal histórico de usuarios."""

    id: UUID
    customer_id: UUID
    user_count: int
    user_subtotal_eur: Decimal
    created_at: datetime

    def __post_init__(self) -> None:
        """Protege las invariantes básicas de la entidad."""

        if (
            isinstance(self.user_count, bool)
            or not isinstance(self.user_count, int)
            or self.user_count < 1
        ):
            raise InvalidSimulationUserCount(self.user_count)

        if not isinstance(self.user_subtotal_eur, Decimal):
            raise InvalidSimulationAmount("El subtotal debe ser un Decimal.")
        if not self.user_subtotal_eur.is_finite() or self.user_subtotal_eur < 0:
            raise InvalidSimulationAmount("El subtotal debe ser un Decimal finito y no negativo.")
