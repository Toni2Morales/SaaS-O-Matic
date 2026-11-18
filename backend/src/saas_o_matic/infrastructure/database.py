"""Configuración de la base de datos SQLAlchemy 2."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATABASE_PATH = BACKEND_ROOT / "var" / "saas_o_matic.sqlite3"
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"


class Base(DeclarativeBase):
    """Base declarativa común de los modelos de persistencia."""


def _normalize_sqlite_url(url: str) -> str:
    """Normaliza una URL SQLite a una ruta absoluta y un único formato.

    Las rutas relativas se interpretan desde ``backend/`` para que el resultado
    no dependa del directorio de trabajo del proceso. Solo se admite SQLite de
    fichero: no se aceptan otros motores, ``:memory:`` ni parámetros de consulta.
    """

    try:
        parsed = make_url(url)
    except ArgumentError as exc:
        raise ValueError("DATABASE_URL no es una URL válida.") from exc

    if parsed.get_backend_name() != "sqlite":
        raise ValueError("DATABASE_URL debe usar SQLite; no se admiten otros motores.")
    if parsed.query:
        raise ValueError("DATABASE_URL no admite parámetros de consulta.")
    if not parsed.database or parsed.database == ":memory:":
        raise ValueError("DATABASE_URL debe apuntar a un fichero SQLite.")

    database_path = Path(parsed.database)
    if not database_path.is_absolute():
        database_path = BACKEND_ROOT / database_path
    return f"sqlite:///{database_path.resolve().as_posix()}"


def resolve_database_url(configured_url: str | None = None) -> str:
    """Resuelve la URL común para el runtime y Alembic.

    Prioridad: ``DATABASE_URL`` del proceso, URL configurada por Alembic y ruta
    predeterminada del backend. No lee ficheros ``.env`` ni abre conexiones.
    """

    environment_url = os.environ.get("DATABASE_URL")
    selected_url = environment_url.strip() if environment_url and environment_url.strip() else None
    if selected_url is None and configured_url is not None:
        selected_url = configured_url.strip() or None
    if selected_url is None:
        return DEFAULT_DATABASE_URL
    return _normalize_sqlite_url(selected_url)


def database_path_from_url(url: str) -> Path:
    """Obtiene la ruta de fichero SQLite de una URL ya resuelta."""

    normalized_url = _normalize_sqlite_url(url)
    return Path(normalized_url.removeprefix("sqlite:///"))


def resolve_database_path(configured_url: str | None = None) -> Path:
    """Resuelve la ruta SQLite que debe usar el runtime."""

    return database_path_from_url(resolve_database_url(configured_url))


def _unicode_casefold(value: str | None) -> str | None:
    """Caseless Unicode sin eliminar acentos ni normalizar equivalencias."""

    return value.casefold() if value is not None else None


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
        dbapi_connection.create_function(
            "unicode_casefold", 1, _unicode_casefold, deterministic=True
        )
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Crea una fábrica de sesiones con expiración desactivada al confirmar."""

    return sessionmaker(bind=engine, expire_on_commit=False)
