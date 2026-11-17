"""Repositorio SQLAlchemy de simulaciones."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from saas_o_matic.domain.simulations.entities import Simulation
from saas_o_matic.infrastructure.simulations.mappers import to_domain, to_model
from saas_o_matic.infrastructure.simulations.models import SimulationModel


class SqlAlchemySimulationRepository:
    """Implementación concreta del puerto de simulaciones sobre SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, simulation: Simulation) -> None:
        """Persiste la simulación y confirma la transacción."""

        try:
            self._session.add(to_model(simulation))
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def get_by_id(self, simulation_id: UUID) -> Simulation | None:
        """Recupera una simulación para comprobaciones internas y pruebas."""

        model = self._session.get(SimulationModel, simulation_id)
        if model is None:
            return None
        return to_domain(model)
