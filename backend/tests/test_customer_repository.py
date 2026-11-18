"""Pruebas de integración del repositorio SQLAlchemy con SQLite aislado."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import cast
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, select

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import DuplicateCustomerTaxId
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    GenericTaxId,
    PlanCode,
    SpanishTaxId,
)
from saas_o_matic.infrastructure.customers.mappers import to_domain
from saas_o_matic.infrastructure.customers.models import CustomerModel
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)


def _customer(
    *,
    customer_id: UUID | None = None,
    tax_id: str = "12345678Z",
) -> Customer:
    return Customer(
        id=customer_id or uuid4(),
        legal_name="Cliente de prueba",
        tax_id=SpanishTaxId.parse(tax_id),
        email="cliente@example.com",
        country=CountryCode.ES,
        plan=PlanCode.STANDARD,
        created_at=datetime.now(UTC),
    )


def test_repository_persists_and_reads_a_customer(migrated_database: Path) -> None:
    """El repositorio persiste los campos aprobados y recupera la entidad."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        with session_factory() as session:
            repository = SqlAlchemyCustomerRepository(session)
            customer = _customer()
            repository.add(customer)

            assert repository.exists_by_tax_id(customer.tax_id, customer.country)

            model = session.scalar(select(CustomerModel))
            assert model is not None
            assert model.tax_id == "12345678Z"
            assert model.country == "ES"
            assert model.plan == "standard"

            restored = to_domain(model)
            assert restored.id == customer.id
            assert restored.tax_id.value == "12345678Z"
            assert restored.country is CountryCode.ES
            assert restored.plan is PlanCode.STANDARD
            assert restored.created_at.tzinfo is UTC
    finally:
        engine.dispose()


def test_repository_checks_customer_existence_by_id(migrated_database: Path) -> None:
    """El repositorio distingue un cliente existente de un UUID desconocido."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        with session_factory() as session:
            repository = SqlAlchemyCustomerRepository(session)
            customer = _customer()
            repository.add(customer)

            assert repository.exists_by_id(customer.id)
            assert not repository.exists_by_id(uuid4())
    finally:
        engine.dispose()


def test_repository_rejects_duplicate_tax_id_for_the_same_country(
    migrated_database: Path,
) -> None:
    """La restricción única de base de datos se traduce a un error de dominio."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)

    try:
        with session_factory() as session:
            repository = SqlAlchemyCustomerRepository(session)
            repository.add(_customer())

            with pytest.raises(DuplicateCustomerTaxId):
                repository.add(_customer(customer_id=uuid4()))

            assert len(session.scalars(select(CustomerModel)).all()) == 1
    finally:
        engine.dispose()


def test_customer_model_requires_plan_and_has_composite_unique_constraint() -> None:
    """El modelo no omite ``plan`` y declara la unicidad fiscal."""

    table = cast(Table, CustomerModel.__table__)

    assert table.c.plan.nullable is False
    constraint_names = {
        constraint.name for constraint in table.constraints if constraint.name is not None
    }
    assert "uq_customers_country_tax_id" in constraint_names


def test_international_customer_reloaded_and_database_uniqueness(migrated_database: Path) -> None:
    """El mapeador reconstruye internacional sin algoritmos ES, también en sesión nueva."""

    engine = create_sqlite_engine(migrated_database)
    factory = create_session_factory(engine)
    customer = replace(_customer(), country=CountryCode.FR, tax_id=GenericTaxId.parse("ab-12 / 34"))
    try:
        with factory() as session:
            repository = SqlAlchemyCustomerRepository(session)
            repository.add(customer)
            repository.add(replace(customer, id=uuid4(), country=CountryCode.PT))
            with pytest.raises(DuplicateCustomerTaxId):
                repository.add(replace(customer, id=uuid4()))
        with factory() as session:
            model = session.get(CustomerModel, customer.id)
            assert model is not None
            restored = to_domain(model)
            assert restored == customer
            assert restored.created_at.tzinfo is UTC
            assert isinstance(restored.tax_id, GenericTaxId)
            assert len(session.scalars(select(CustomerModel)).all()) == 2
    finally:
        engine.dispose()
