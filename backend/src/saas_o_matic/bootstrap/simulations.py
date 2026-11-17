"""Composición del módulo de simulaciones."""

from __future__ import annotations

from sqlalchemy.orm import Session

from saas_o_matic.application.simulations.use_cases import CreateSimulation
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository
from saas_o_matic.infrastructure.simulations.repositories import (
    SqlAlchemySimulationRepository,
)


def build_simulation_use_case(session: Session) -> CreateSimulation:
    """Construye el caso de uso con repositorios que comparten la sesión."""

    return CreateSimulation(
        simulations=SqlAlchemySimulationRepository(session),
        customers=SqlAlchemyCustomerRepository(session),
    )
