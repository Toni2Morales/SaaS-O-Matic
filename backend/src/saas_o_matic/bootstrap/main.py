"""Punto de entrada ASGI y composition root provisional."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.queries import CustomerQueries
from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.application.simulations.queries import SimulationQueries
from saas_o_matic.application.simulations.use_cases import CreateSimulation, PreviewSimulation
from saas_o_matic.bootstrap.customers import build_customer_queries, build_customer_use_case
from saas_o_matic.bootstrap.simulations import (
    build_preview_use_case,
    build_simulation_queries,
    build_simulation_use_case,
)
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
    resolve_database_path,
)
from saas_o_matic.presentation.app import create_app
from saas_o_matic.presentation.customers.dependencies import (
    get_create_customer_use_case,
    get_customer_queries,
)
from saas_o_matic.presentation.simulations.dependencies import (
    get_create_simulation_use_case,
    get_preview_simulation_use_case,
    get_simulation_queries,
)

_session_factory: sessionmaker[Session] | None = None


def _get_session_factory() -> sessionmaker[Session]:
    """Crea la fábrica de sesiones de forma perezosa.

    Así, importar la aplicación no crea el directorio ni el fichero SQLite.
    La ruta se resuelve con la misma configuración que Alembic.
    """

    global _session_factory
    if _session_factory is None:
        engine = create_sqlite_engine(resolve_database_path())
        _session_factory = create_session_factory(engine)
    return _session_factory


def _customer_use_case_dependency() -> Iterator[CreateCustomer]:
    """Proporciona un caso de uso con una sesión por petición."""

    with _get_session_factory()() as session:
        yield build_customer_use_case(session)


def _simulation_use_case_dependency() -> Iterator[CreateSimulation]:
    """Proporciona el caso de uso de simulaciones con una sesión por petición."""

    with _get_session_factory()() as session:
        yield build_simulation_use_case(session)


def _customer_queries_dependency() -> Iterator[CustomerQueries]:
    with _get_session_factory()() as session:
        yield build_customer_queries(session)


def _simulation_queries_dependency() -> Iterator[SimulationQueries]:
    with _get_session_factory()() as session:
        yield build_simulation_queries(session)


def _preview_use_case_dependency() -> Iterator[PreviewSimulation]:
    with _get_session_factory()() as session:
        yield build_preview_use_case(session)


app = create_app()
app.dependency_overrides[get_create_customer_use_case] = _customer_use_case_dependency
app.dependency_overrides[get_create_simulation_use_case] = _simulation_use_case_dependency
app.dependency_overrides[get_customer_queries] = _customer_queries_dependency
app.dependency_overrides[get_simulation_queries] = _simulation_queries_dependency
app.dependency_overrides[get_preview_simulation_use_case] = _preview_use_case_dependency
