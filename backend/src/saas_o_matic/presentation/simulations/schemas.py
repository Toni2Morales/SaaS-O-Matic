"""Esquemas Pydantic de la API de simulaciones."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, date, datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from saas_o_matic.application.simulations.dto import (
    MAX_API_CALLS_PER_MONTH,
    MAX_SIMULATION_USER_COUNT,
    MAX_STORAGE_GB,
    Currency,
    HistoricalSimulationResult,
    PreviewSimulationResult,
    SimulationResult,
)

UserCount = Annotated[
    int,
    Field(strict=True, ge=0, le=MAX_SIMULATION_USER_COUNT),
]


class SimulationCreateRequest(BaseModel):
    """Datos de entrada de la creación de una simulación."""

    model_config = ConfigDict(extra="forbid")

    customer_id: UUID
    user_count: UserCount
    storage_gb: Annotated[int, Field(strict=True, ge=0, le=MAX_STORAGE_GB)]
    api_calls_per_month: Annotated[int, Field(strict=True, ge=0, le=MAX_API_CALLS_PER_MONTH)]
    display_currency: Currency = Currency.EUR


class SimulationPreviewResponse(BaseModel):
    """Cálculo no persistido; no tiene id ni created_at de simulación."""

    customer_id: UUID
    user_count: int
    user_subtotal_eur: str
    storage_gb: int
    api_calls_per_month: int
    billing_period: Literal["monthly"]
    tax_country: str
    tax_rate: str
    tax_source: str
    tax_catalog_version: str
    tax_verified_on: date
    tax_territory: str
    tax_effective_from: date | None
    tax_amount_eur: str
    total_eur: str
    display_currency: Currency
    exchange_rate: str
    exchange_rate_date: date | None
    exchange_rate_obtained_at: datetime
    exchange_rate_source: str
    converted_total: str

    @field_serializer("exchange_rate_obtained_at")
    def serialize_created_at(self, value: datetime) -> str:
        """Serializa la fecha en ISO 8601 UTC con sufijo ``Z``."""

        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class SimulationResponse(SimulationPreviewResponse):
    """Registro creado con todos los datos obligatorios actuales."""

    id: UUID
    created_at: datetime

    @field_serializer("created_at")
    def serialize_record_created_at(self, value: datetime) -> str:
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class HistoricalSimulationResponse(BaseModel):
    """Cada concepto desconocido se devuelve NULL, no cero ni EUR inventado."""

    id: UUID
    customer_id: UUID
    user_count: int
    storage_gb: int | None
    api_calls_per_month: int | None
    billing_period: Literal["monthly"]
    user_subtotal_eur: str
    created_at: datetime
    tax_country: str | None
    tax_rate: str | None
    tax_source: str | None
    tax_catalog_version: str | None
    tax_verified_on: date | None
    tax_territory: str | None
    tax_effective_from: date | None
    tax_amount_eur: str | None
    total_eur: str | None
    display_currency: Currency | None
    exchange_rate: str | None
    exchange_rate_date: date | None
    exchange_rate_obtained_at: datetime | None
    exchange_rate_source: str | None
    converted_total: str | None

    @field_serializer("created_at", "exchange_rate_obtained_at")
    def serialize_utc(self, value: datetime | None) -> str | None:
        return (
            value.astimezone(UTC).isoformat().replace("+00:00", "Z") if value is not None else None
        )


class SimulationHistoryPageResponse(BaseModel):
    items: list[HistoricalSimulationResponse]
    total: int
    limit: int
    offset: int


def simulation_values(
    result: SimulationResult | PreviewSimulationResult | HistoricalSimulationResult,
) -> dict[str, Any]:
    """Aplana DTO de aplicación sin acceder al dominio desde presentación."""

    values = asdict(result)
    calculation = values.pop("calculation")
    calculation.pop("schema_version", None)
    return {**values, **calculation}
