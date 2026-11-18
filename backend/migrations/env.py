"""Configuración de Alembic para SaaS-O-Matic."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from saas_o_matic.infrastructure.customers import models as customer_models  # noqa: F401
from saas_o_matic.infrastructure.database import (
    Base,
    database_path_from_url,
    resolve_database_url,
)
from saas_o_matic.infrastructure.simulations import models as simulation_models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _database_url() -> str:
    """Obtiene la URL común, permitiendo sustituirla por entorno."""

    return resolve_database_url(config.get_main_option("sqlalchemy.url"))


def _ensure_sqlite_parent() -> None:
    """Crea el directorio de la base SQLite si la URL apunta a un fichero."""

    database_path_from_url(_database_url()).parent.mkdir(parents=True, exist_ok=True)


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo offline."""

    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo online."""

    _ensure_sqlite_parent()
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
