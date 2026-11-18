"""Errores de aplicación del módulo de simulaciones."""

from __future__ import annotations

from uuid import UUID


class SimulationApplicationError(Exception):
    """Error base de la aplicación de simulaciones."""


class ConversionUnavailable(SimulationApplicationError):
    """No existe una referencia de divisas válida para completar el cálculo."""


class InvalidSimulationData(SimulationApplicationError):
    """Los datos de la simulación no superan una validación."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(message)


class SimulationCustomerNotFound(SimulationApplicationError):
    """El cliente indicado no está registrado."""

    def __init__(self, customer_id: UUID) -> None:
        self.customer_id = customer_id
        super().__init__(f"No existe un cliente con identificador {customer_id}.")
