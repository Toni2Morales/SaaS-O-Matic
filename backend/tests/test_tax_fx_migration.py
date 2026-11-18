"""Snapshot nullable, conservación byte a byte de históricos y downgrade protegido."""

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text

from saas_o_matic.domain.customers.value_objects import CountryCode
from saas_o_matic.domain.simulations.calculation import Currency, ExchangeQuote, calculate_monthly
from saas_o_matic.infrastructure.database import create_sqlite_engine
from saas_o_matic.infrastructure.tax_catalog import configured_tax_catalog


def test_upgrade_historical_and_guarded_downgrade(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "taxfx.sqlite3"
    url = f"sqlite:///{path.as_posix()}"
    monkeypatch.setenv("DATABASE_URL", url)
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "0003_international_simulations")
    engine = create_sqlite_engine(path)
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO customers VALUES (:id,'Empresa','12345678Z',"
                    "'a@example.com','ES','standard','2026-11-16 00:00:00.123456')"
                ),
                {"id": "a" * 32},
            )
            connection.execute(
                text(
                    "INSERT INTO simulations "
                    "(id,customer_id,user_count,user_subtotal_eur,created_at,storage_gb,"
                    "api_calls_per_month,billing_period) "
                    "VALUES (:id,:customer,15,'140.00','2026-11-16 00:00:00.123456',"
                    "NULL,NULL,'monthly')"
                ),
                {"id": "b" * 32, "customer": "a" * 32},
            )
        with engine.connect() as connection:
            old = tuple(connection.execute(text("SELECT * FROM simulations")).one())
        command.upgrade(config, "head")
        with engine.connect() as connection:
            assert tuple(connection.execute(text("SELECT * FROM simulations")).one()) == (
                *old,
                None,
            )
        command.downgrade(config, "0003_international_simulations")
        command.upgrade(config, "head")
        snapshot = calculate_monthly(
            Decimal("140.00"),
            configured_tax_catalog().for_country(CountryCode.ES),
            ExchangeQuote(Currency.EUR, Decimal("1"), None, datetime.now(UTC), "identity"),
        ).snapshot()
        with engine.begin() as connection:
            connection.execute(
                text("UPDATE simulations SET calculation_snapshot=:snapshot"),
                {"snapshot": json.dumps(snapshot)},
            )
        with pytest.raises(RuntimeError, match="Downgrade bloqueado"):
            command.downgrade(config, "0003_international_simulations")
        with engine.connect() as connection:
            assert (
                json.loads(
                    connection.execute(
                        text("SELECT calculation_snapshot FROM simulations")
                    ).scalar_one()
                )
                == snapshot
            )
            assert (
                connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
                == "0004_add_simulation_taxes_and_fx"
            )
            assert connection.exec_driver_sql("PRAGMA foreign_key_check").all() == []
    finally:
        engine.dispose()
