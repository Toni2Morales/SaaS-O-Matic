"""Pruebas de integración del repositorio SQLAlchemy de simulaciones."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import cast
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, insert, select, text
from sqlalchemy.exc import IntegrityError

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    PlanCode,
    SpanishTaxId,
)
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
from saas_o_matic.domain.simulations.entities import Simulation, format_eur_amount
from saas_o_matic.infrastructure.customers.repositories import (
    SqlAlchemyCustomerRepository,
)
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)
from saas_o_matic.infrastructure.simulations.models import SimulationModel
from saas_o_matic.infrastructure.simulations.repositories import (
    SqlAlchemySimulationRepository,
)


def _customer(*, customer_id: UUID | None = None, tax_id: str = "B12345674") -> Customer:
    return Customer(
        id=customer_id or uuid4(),
        legal_name="Cliente de simulación",
        tax_id=SpanishTaxId.parse(tax_id),
        email="cliente@example.com",
        country=CountryCode.ES,
        plan=PlanCode.STANDARD,
        created_at=datetime.now(UTC),
    )


def _simulation(
    *,
    customer_id: UUID,
    user_count: int = 100,
    user_subtotal_eur: Decimal | None = None,
) -> Simulation:
    return Simulation(
        id=uuid4(),
        customer_id=customer_id,
        user_count=user_count,
        user_subtotal_eur=user_subtotal_eur
        if user_subtotal_eur is not None
        else calculate_user_subtotal(user_count),
        created_at=datetime.now(UTC),
    )


def test_repository_persists_and_recovers_the_exact_amount(
    migrated_database: Path,
) -> None:
    """El repositorio guarda texto canónico y recupera el Decimal exacto."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        customer = _customer()
        simulation = _simulation(customer_id=customer.id)
        with session_factory() as session:
            SqlAlchemyCustomerRepository(session).add(customer)
            repository = SqlAlchemySimulationRepository(session)
            repository.add(simulation)

            stored = session.scalar(select(SimulationModel))
            assert stored is not None
            assert stored.user_subtotal_eur == "670.00"
            assert isinstance(stored.user_subtotal_eur, str)

            restored = repository.get_by_id(simulation.id)
            assert restored is not None
            assert restored.id == simulation.id
            assert restored.customer_id == customer.id
            assert restored.user_count == 100
            assert restored.user_subtotal_eur == Decimal("670.00")
            assert restored.created_at.tzinfo is UTC
    finally:
        engine.dispose()


def test_physical_text_and_new_session_reconstruction(migrated_database: Path) -> None:
    """Comprueba tipo SQLite real, Decimal exacto y fecha UTC tras cerrar sesión."""

    engine = create_sqlite_engine(migrated_database)
    factory = create_session_factory(engine)
    customer = _customer()
    simulation = _simulation(customer_id=customer.id, user_count=15)
    try:
        with factory() as session:
            SqlAlchemyCustomerRepository(session).add(customer)
            SqlAlchemySimulationRepository(session).add(simulation)
        with engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT typeof(user_subtotal_eur), user_subtotal_eur, "
                    "storage_gb, api_calls_per_month, billing_period FROM simulations"
                )
            ).one()
            assert tuple(row) == ("text", "140.00", None, None, "monthly")
        with factory() as session:
            restored = SqlAlchemySimulationRepository(session).get_by_id(simulation.id)
            assert restored is not None
            assert restored.user_subtotal_eur.as_tuple() == Decimal("140.00").as_tuple()
            assert restored.created_at == simulation.created_at
            assert restored.created_at.tzinfo is UTC
            assert restored.storage_gb is None
    finally:
        engine.dispose()


def test_repository_persists_the_maximum_technical_count(migrated_database: Path) -> None:
    """El máximo autorizado se persiste con su subtotal exacto."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        customer = _customer()
        simulation = _simulation(customer_id=customer.id, user_count=1_000_000)
        with session_factory() as session:
            SqlAlchemyCustomerRepository(session).add(customer)
            repository = SqlAlchemySimulationRepository(session)
            repository.add(simulation)

            stored = session.scalar(select(SimulationModel))
            assert stored is not None
            assert stored.user_count == 1_000_000
            assert stored.user_subtotal_eur == "5000170.00"

            restored = repository.get_by_id(simulation.id)
            assert restored is not None
            assert restored.user_subtotal_eur == Decimal("5000170.00")
            assert format_eur_amount(restored.user_subtotal_eur) == "5000170.00"
    finally:
        engine.dispose()


def test_foreign_keys_are_enabled_and_enforced(migrated_database: Path) -> None:
    """La conexión aplica PRAGMA y rechaza una simulación huérfana."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        with engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1

        with session_factory() as session:
            repository = SqlAlchemySimulationRepository(session)
            orphan = _simulation(customer_id=uuid4())

            with pytest.raises(IntegrityError):
                repository.add(orphan)

            assert session.scalars(select(SimulationModel)).all() == []
    finally:
        engine.dispose()


def test_database_check_rejects_user_count_outside_the_range(
    migrated_database: Path,
) -> None:
    """El CHECK de SQLite protege el rango aunque se inserte directamente."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        customer = _customer()
        with session_factory() as session:
            SqlAlchemyCustomerRepository(session).add(customer)

            with pytest.raises(IntegrityError):
                session.execute(
                    insert(SimulationModel).values(
                        id=uuid4(),
                        customer_id=customer.id,
                        user_count=-1,
                        user_subtotal_eur="0.00",
                        created_at=datetime.now(UTC),
                    )
                )
            session.rollback()

            assert session.scalars(select(SimulationModel)).all() == []
    finally:
        engine.dispose()


def test_simulation_model_declares_the_expected_constraints() -> None:
    """El modelo declara FK, CHECK y columnas no nulas."""

    table = cast(Table, SimulationModel.__table__)
    constraint_names = {
        constraint.name for constraint in table.constraints if constraint.name is not None
    }

    assert table.c.customer_id.nullable is False
    assert table.c.user_count.nullable is False
    assert table.c.user_subtotal_eur.nullable is False
    assert table.c.created_at.nullable is False
    assert "fk_simulations_customer_id" in constraint_names
    assert "ck_simulations_user_count_range" in constraint_names
