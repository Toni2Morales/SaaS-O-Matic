"""Pruebas de la migración inicial de clientes con Alembic."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import DuplicateCustomerTaxId
from saas_o_matic.domain.customers.value_objects import CountryCode, PlanCode, SpanishTaxId
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository
from saas_o_matic.infrastructure.database import create_session_factory

ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"
EXPECTED_REVISION = "0002_create_simulations"


def _config(database_url: str) -> Config:
    config = Config(str(ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _customer(tax_id: str = "B12345674") -> Customer:
    return Customer(
        id=uuid4(),
        legal_name="Empresa de prueba",
        tax_id=SpanishTaxId.parse(tax_id),
        email="empresa@example.com",
        country=CountryCode.ES,
        plan=PlanCode.STANDARD,
        created_at=datetime.now(UTC),
    )


def test_alembic_upgrade_schema_persistence_downgrade_and_reupgrade(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Valida el ciclo completo de la migración sobre una base temporal."""

    database_path = tmp_path / "migration.sqlite3"
    database_url = f"sqlite:///{database_path.as_posix()}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    config = _config(database_url)

    command.upgrade(config, "head")

    engine = create_engine(database_url)
    try:
        inspector = inspect(engine)
        assert {"customers", "simulations"} <= set(inspector.get_table_names())

        columns = {column["name"]: column for column in inspector.get_columns("customers")}
        assert set(columns) == {
            "id",
            "legal_name",
            "tax_id",
            "email",
            "country",
            "plan",
            "created_at",
        }
        for field in ("id", "legal_name", "tax_id", "email", "country", "plan", "created_at"):
            assert columns[field]["nullable"] is False

        unique_constraints = inspector.get_unique_constraints("customers")
        assert any(
            constraint["name"] == "uq_customers_country_tax_id"
            and set(constraint["column_names"]) == {"country", "tax_id"}
            for constraint in unique_constraints
        )

        simulation_columns = {
            column["name"]: column for column in inspector.get_columns("simulations")
        }
        assert set(simulation_columns) == {
            "id",
            "customer_id",
            "user_count",
            "user_subtotal_eur",
            "created_at",
        }
        for field in ("id", "customer_id", "user_count", "user_subtotal_eur", "created_at"):
            assert simulation_columns[field]["nullable"] is False

        check_constraints = inspector.get_check_constraints("simulations")
        assert any(
            constraint["name"] == "ck_simulations_user_count_range"
            and "user_count" in constraint["sqltext"]
            for constraint in check_constraints
        )

        foreign_keys = inspector.get_foreign_keys("simulations")
        assert any(
            foreign_key["name"] == "fk_simulations_customer_id"
            and foreign_key["constrained_columns"] == ["customer_id"]
            and foreign_key["referred_table"] == "customers"
            and foreign_key["referred_columns"] == ["id"]
            for foreign_key in foreign_keys
        )

        with engine.connect() as connection:
            revision = connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one()
        assert revision == EXPECTED_REVISION

        session_factory = create_session_factory(engine)
        customer = _customer()
        with session_factory() as session:
            repository = SqlAlchemyCustomerRepository(session)
            repository.add(customer)
            assert repository.exists_by_tax_id(customer.tax_id, customer.country)

            with pytest.raises(DuplicateCustomerTaxId):
                repository.add(_customer())
    finally:
        engine.dispose()

    command.downgrade(config, "0001_create_customers")

    engine = create_engine(database_url)
    try:
        tables = inspect(engine).get_table_names()
        assert "customers" in tables
        assert "simulations" not in tables
        with engine.connect() as connection:
            assert connection.execute(text("SELECT COUNT(*) FROM customers")).scalar_one() == 1
    finally:
        engine.dispose()

    command.downgrade(config, "base")

    engine = create_engine(database_url)
    try:
        assert "customers" not in inspect(engine).get_table_names()
    finally:
        engine.dispose()

    command.upgrade(config, "head")

    engine = create_engine(database_url)
    try:
        assert {"customers", "simulations"} <= set(inspect(engine).get_table_names())
    finally:
        engine.dispose()
