"""DTOs del caso de uso de creación de simulaciones."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from saas_o_matic.application.pagination import DEFAULT_PAGE_LIMIT
from saas_o_matic.domain.simulations.calculation import Currency as Currency

MAX_SIMULATION_USER_COUNT = 1_000_000
MAX_STORAGE_GB = 1_000_000
MAX_API_CALLS_PER_MONTH = 1_000_000_000


@dataclass(frozen=True, slots=True)
class CreateSimulationCommand:
    """Datos de entrada para crear una simulación."""

    customer_id: UUID
    user_count: int
    storage_gb: int
    api_calls_per_month: int
    display_currency: Currency = Currency.EUR


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Representación de salida de una simulación creada."""

    id: UUID
    customer_id: UUID
    user_count: int
    user_subtotal_eur: str
    created_at: datetime
    storage_gb: int
    api_calls_per_month: int
    billing_period: Literal["monthly"]
    calculation: dict[str, str | None]


@dataclass(frozen=True, slots=True)
class PreviewSimulationResult:
    customer_id: UUID
    user_count: int
    storage_gb: int
    api_calls_per_month: int
    billing_period: Literal["monthly"]
    user_subtotal_eur: str
    calculation: dict[str, str | None]


@dataclass(frozen=True, slots=True)
class HistoricalSimulationResult:
    id: UUID
    customer_id: UUID
    user_count: int
    storage_gb: int | None
    api_calls_per_month: int | None
    billing_period: Literal["monthly"]
    user_subtotal_eur: str
    created_at: datetime
    calculation: dict[str, str | None]


@dataclass(frozen=True, slots=True)
class SimulationHistoryQuery:
    customer_id: UUID
    limit: int = DEFAULT_PAGE_LIMIT
    offset: int = 0


@dataclass(frozen=True, slots=True)
class SimulationHistoryResult:
    items: list[HistoricalSimulationResult]
    total: int
    limit: int
    offset: int
