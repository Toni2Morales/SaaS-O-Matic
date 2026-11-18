"""Repositorio SQLAlchemy de simulaciones."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
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

    def list_for_customer(
        self,
        customer_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> tuple[list[Simulation], int]:
        """No consulta catálogos ni divisas; reconstruye la página persistida."""

        predicate = SimulationModel.customer_id == customer_id
        with self._session.no_autoflush:
            total = (
                self._session.scalar(
                    select(func.count()).select_from(SimulationModel).where(predicate)
                )
                or 0
            )
            if offset >= total:
                return [], total
            models = self._session.scalars(
                select(SimulationModel)
                .where(predicate)
                .order_by(
                    SimulationModel.created_at.desc(),
                    SimulationModel.id.desc(),
                )
                .limit(limit)
                .offset(offset)
            ).all()
            return [to_domain(model) for model in models], total
