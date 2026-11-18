"""Migración poblada PR #5 → TASK036 y downgrade sin pérdidas silenciosas."""

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from saas_o_matic.infrastructure.database import create_sqlite_engine

OLD = "0002_create_simulations"


def _config(path: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    url = f"sqlite:///{path.as_posix()}"
    monkeypatch.setenv("DATABASE_URL", url)
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", url)
    return config


def _seed(path: Path) -> None:
    engine = create_sqlite_engine(path)
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO customers VALUES (:id, 'Empresa', '12345678Z', "
                    "'a@example.com', 'ES', 'standard', '2026-11-17 10:00:00.123456')"
                ),
                {"id": "a" * 32},
            )
            connection.execute(
                text(
                    "INSERT INTO simulations VALUES (:id, :customer, 15, '140.00', "
                    "'2026-11-17 10:01:00.123456')"
                ),
                {"id": "b" * 32, "customer": "a" * 32},
            )
    finally:
        engine.dispose()


def test_upgrade_preserves_historical_values_and_reversible_cycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "historical.sqlite3"
    config = _config(path, monkeypatch)
    command.upgrade(config, OLD)
    _seed(path)
    engine = create_sqlite_engine(path)
    try:
        with engine.connect() as connection:
            old_customer = tuple(connection.execute(text("SELECT * FROM customers")).one())
            old_simulation = tuple(connection.execute(text("SELECT * FROM simulations")).one())
        command.upgrade(config, "head")
        with engine.connect() as connection:
            assert tuple(connection.execute(text("SELECT * FROM customers")).one()) == old_customer
            row = tuple(
                connection.execute(
                    text(
                        "SELECT id, customer_id, user_count, user_subtotal_eur, created_at, "
                        "storage_gb, api_calls_per_month, billing_period FROM simulations"
                    )
                ).one()
            )
            assert row == (*old_simulation, None, None, "monthly")
            assert connection.exec_driver_sql("PRAGMA foreign_key_check").all() == []
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
        command.downgrade(config, OLD)
        with engine.connect() as connection:
            assert (
                tuple(connection.execute(text("SELECT * FROM simulations")).one()) == old_simulation
            )
        command.upgrade(config, "head")
    finally:
        engine.dispose()


@pytest.mark.parametrize("incompatibility", ["international", "zero", "consumption"])
def test_downgrade_fails_before_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    incompatibility: str,
) -> None:
    path = tmp_path / "blocked.sqlite3"
    config = _config(path, monkeypatch)
    command.upgrade(config, OLD)
    _seed(path)
    command.upgrade(config, "head")
    engine = create_sqlite_engine(path)
    try:
        with engine.begin() as connection:
            if incompatibility == "international":
                connection.execute(text("UPDATE customers SET country='FR'"))
            elif incompatibility == "zero":
                connection.execute(
                    text("UPDATE simulations SET user_count=0, user_subtotal_eur='0.00'")
                )
            else:
                connection.execute(text("UPDATE simulations SET storage_gb=0"))
        with pytest.raises(RuntimeError, match="Downgrade bloqueado"):
            command.downgrade(config, OLD)
        with engine.connect() as connection:
            assert connection.execute(text("SELECT COUNT(*) FROM simulations")).scalar_one() == 1
            assert (
                connection.execute(text("SELECT billing_period FROM simulations")).scalar_one()
                == "monthly"
            )
            assert (
                connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
                == "0003_international_simulations"
            )
            assert connection.exec_driver_sql("PRAGMA foreign_key_check").all() == []
    finally:
        engine.dispose()


@pytest.mark.parametrize(
    "assignment",
    [
        "user_count=-1",
        "user_count=1000001",
        "user_count=0.5",
        "storage_gb=-1",
        "storage_gb=1000001",
        "storage_gb=0.5",
        "api_calls_per_month=-1",
        "api_calls_per_month=1000000001",
        "api_calls_per_month=0.5",
        "billing_period='yearly'",
    ],
)
def test_database_constraints(migrated_database: Path, assignment: str) -> None:
    engine = create_sqlite_engine(migrated_database)
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO customers VALUES (:id, 'Empresa', 'SAME', "
                    "'a@example.com', 'FR', 'standard', '2026-11-17')"
                ),
                {"id": "a" * 32},
            )
            connection.execute(
                text(
                    "INSERT INTO customers VALUES (:id, 'Empresa', 'SAME', "
                    "'a@example.com', 'PT', 'standard', '2026-11-17')"
                ),
                {"id": "c" * 32},
            )
            connection.execute(
                text(
                    "INSERT INTO simulations "
                    "(id, customer_id, user_count, user_subtotal_eur, created_at) "
                    "VALUES (:id, :customer, 0, '0.00', '2026-11-17')"
                ),
                {"id": "b" * 32, "customer": "a" * 32},
            )
        with engine.begin() as connection, pytest.raises(IntegrityError):
            connection.execute(text(f"UPDATE simulations SET {assignment}"))
        with engine.begin() as connection, pytest.raises(IntegrityError):
            connection.execute(text("UPDATE customers SET country='FR' WHERE country='PT'"))
        with engine.begin() as connection, pytest.raises(IntegrityError):
            connection.execute(text("UPDATE simulations SET customer_id=:id"), {"id": "d" * 32})
    finally:
        engine.dispose()
