"""DTOs del caso de uso de creación de simulaciones."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

MAX_SIMULATION_USER_COUNT = 1_000_000


@dataclass(frozen=True, slots=True)
class CreateSimulationCommand:
    """Datos de entrada para crear una simulación."""

    customer_id: UUID
    user_count: int


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Representación de salida de una simulación creada."""

    id: UUID
    customer_id: UUID
    user_count: int
    user_subtotal_eur: str
    created_at: datetime
