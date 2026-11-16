"""Configuración de la base de datos SQLAlchemy 2."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa común de los modelos de persistencia."""


def create_sqlite_engine(database_path: Path) -> Engine:
    """Crea un motor SQLite para una ruta de fichero concreta."""

    database_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        f"sqlite:///{database_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Crea una fábrica de sesiones con expiración desactivada al confirmar."""

    return sessionmaker(bind=engine, expire_on_commit=False)
