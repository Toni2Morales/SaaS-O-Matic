"""Configuración de la base de datos SQLAlchemy 2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa común de los modelos de persistencia."""


def create_sqlite_engine(database_path: Path) -> Engine:
    """Crea un motor SQLite para una ruta de fichero concreta.

    SQLite no aplica claves foráneas por defecto. El listener activa la
    comprobación en cada conexión nueva del motor.
    """

    database_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(
        dbapi_connection: Any,
        _connection_record: Any,
    ) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Crea una fábrica de sesiones con expiración desactivada al confirmar."""

    return sessionmaker(bind=engine, expire_on_commit=False)
