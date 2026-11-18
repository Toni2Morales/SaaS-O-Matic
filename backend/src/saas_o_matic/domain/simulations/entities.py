"""Entidades y utilidades monetarias del dominio de simulaciones."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Context, Decimal, DecimalException, localcontext
from typing import Literal
from uuid import UUID

from saas_o_matic.domain.simulations.calculation import MonthlyCalculation

_CENT = Decimal("0.01")


class SimulationDomainError(ValueError):
    """Error base del dominio de simulaciones."""


class InvalidSimulationUserCount(SimulationDomainError):
    """El número de usuarios no es un entero no negativo."""

    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__("El número de usuarios debe ser un entero no negativo.")


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
        with localcontext(Context()) as context:
            context.clear_traps()
            context.prec = max(28, len(value.as_tuple().digits) + 2, value.adjusted() + 3)
            quantized = value.quantize(_CENT)
            if not quantized.is_finite():
                raise InvalidSimulationAmount("El importe no es representable.")
    except DecimalException as exc:
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
    storage_gb: int | None = None
    api_calls_per_month: int | None = None
    billing_period: Literal["monthly"] = "monthly"
    calculation: MonthlyCalculation | None = None

    def __post_init__(self) -> None:
        """Protege las invariantes básicas de la entidad."""

        if (
            isinstance(self.user_count, bool)
            or not isinstance(self.user_count, int)
            or self.user_count < 0
        ):
            raise InvalidSimulationUserCount(self.user_count)

        for name, value in (
            ("storage_gb", self.storage_gb),
            ("api_calls_per_month", self.api_calls_per_month),
        ):
            if value is not None and (type(value) is not int or value < 0):
                raise SimulationDomainError(f"{name} debe ser un entero no negativo o nulo.")
        if self.billing_period != "monthly":
            raise SimulationDomainError("La periodicidad debe ser mensual.")

        if not isinstance(self.user_subtotal_eur, Decimal):
            raise InvalidSimulationAmount("El subtotal debe ser un Decimal.")
        if not self.user_subtotal_eur.is_finite() or self.user_subtotal_eur < 0:
            raise InvalidSimulationAmount("El subtotal debe ser un Decimal finito y no negativo.")
        if self.calculation is not None:
            self.calculation.validate_against(self.user_subtotal_eur)
