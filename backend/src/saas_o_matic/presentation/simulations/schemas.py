"""Esquemas Pydantic de la API de simulaciones."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from saas_o_matic.application.simulations.dto import MAX_SIMULATION_USER_COUNT

UserCount = Annotated[
    int,
    Field(strict=True, ge=1, le=MAX_SIMULATION_USER_COUNT),
]


class SimulationCreateRequest(BaseModel):
    """Datos de entrada de la creación de una simulación."""

    model_config = ConfigDict(extra="ignore")

    customer_id: UUID
    user_count: UserCount


class SimulationResponse(BaseModel):
    """Representación de una simulación creada."""

    id: UUID
    customer_id: UUID
    user_count: int
    user_subtotal_eur: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        """Serializa la fecha en ISO 8601 UTC con sufijo ``Z``."""

        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
