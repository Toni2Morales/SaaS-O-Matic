"""Conversión entre el modelo de persistencia y la entidad de simulación."""

from __future__ import annotations

from datetime import UTC
from decimal import Decimal

from saas_o_matic.domain.simulations.entities import Simulation, format_eur_amount
from saas_o_matic.infrastructure.simulations.models import SimulationModel


def to_domain(model: SimulationModel) -> Simulation:
    """Convierte una fila persistida en la entidad de dominio."""

    created_at = model.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    return Simulation(
        id=model.id,
        customer_id=model.customer_id,
        user_count=model.user_count,
        user_subtotal_eur=Decimal(model.user_subtotal_eur),
        created_at=created_at,
    )


def to_model(simulation: Simulation) -> SimulationModel:
    """Convierte una entidad de dominio en su modelo de persistencia."""

    return SimulationModel(
        id=simulation.id,
        customer_id=simulation.customer_id,
        user_count=simulation.user_count,
        user_subtotal_eur=format_eur_amount(simulation.user_subtotal_eur),
        created_at=simulation.created_at,
    )
