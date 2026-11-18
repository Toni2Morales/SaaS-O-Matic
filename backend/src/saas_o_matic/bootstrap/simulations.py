"""Composición del módulo de simulaciones."""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy.orm import Session

from saas_o_matic.application.simulations.estimator import MonthlyEstimator
from saas_o_matic.application.simulations.queries import SimulationQueries
from saas_o_matic.application.simulations.use_cases import CreateSimulation, PreviewSimulation
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository
from saas_o_matic.infrastructure.frankfurter import FrankfurterRates
from saas_o_matic.infrastructure.simulations.repositories import (
    SqlAlchemySimulationRepository,
)
from saas_o_matic.infrastructure.tax_catalog import configured_tax_catalog


@lru_cache(maxsize=1)
def shared_estimator() -> MonthlyEstimator:
    """Una caché por proceso; urllib abre y cierra cada respuesta, sin cliente global."""

    return MonthlyEstimator(configured_tax_catalog(), FrankfurterRates())


def build_simulation_use_case(
    session: Session,
    estimator: MonthlyEstimator | None = None,
) -> CreateSimulation:
    """Construye el caso de uso con repositorios que comparten la sesión."""

    return CreateSimulation(
        simulations=SqlAlchemySimulationRepository(session),
        customers=SqlAlchemyCustomerRepository(session),
        estimator=estimator if estimator is not None else shared_estimator(),
    )


def build_preview_use_case(
    session: Session,
    estimator: MonthlyEstimator | None = None,
) -> PreviewSimulation:
    return PreviewSimulation(
        customers=SqlAlchemyCustomerRepository(session),
        estimator=estimator if estimator is not None else shared_estimator(),
    )


def build_simulation_queries(session: Session) -> SimulationQueries:
    return SimulationQueries(
        customers=SqlAlchemyCustomerRepository(session),
        simulations=SqlAlchemySimulationRepository(session),
    )
