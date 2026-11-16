"""Punto de entrada ASGI y composition root provisional."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.bootstrap.customers import build_customer_use_case
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)
from saas_o_matic.presentation.app import create_app
from saas_o_matic.presentation.customers.dependencies import get_create_customer_use_case

_DATABASE_PATH = Path(__file__).resolve().parents[3] / "var" / "saas_o_matic.sqlite3"
_session_factory: sessionmaker[Session] | None = None


def _get_session_factory() -> sessionmaker[Session]:
    """Crea la fábrica de sesiones de forma perezosa.

    Así, importar la aplicación no crea el directorio ni el fichero SQLite.
    """

    global _session_factory
    if _session_factory is None:
        engine = create_sqlite_engine(_DATABASE_PATH)
        _session_factory = create_session_factory(engine)
    return _session_factory


def _customer_use_case_dependency() -> Iterator[CreateCustomer]:
    """Proporciona un caso de uso con una sesión por petición."""

    with _get_session_factory()() as session:
        yield build_customer_use_case(session)


app = create_app()
app.dependency_overrides[get_create_customer_use_case] = _customer_use_case_dependency
