"""Pruebas de la API HTTP de creación de simulaciones."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.application.simulations.use_cases import CreateSimulation
from saas_o_matic.bootstrap.customers import build_customer_use_case
from saas_o_matic.bootstrap.simulations import build_simulation_use_case
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    PlanCode,
    SpanishTaxId,
)
from saas_o_matic.infrastructure.customers.repositories import (
    SqlAlchemyCustomerRepository,
)
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)
from saas_o_matic.infrastructure.simulations.models import SimulationModel
from saas_o_matic.presentation.app import create_app
from saas_o_matic.presentation.customers.dependencies import get_create_customer_use_case
from saas_o_matic.presentation.simulations.dependencies import (
    get_create_simulation_use_case,
)


@dataclass(frozen=True)
class SimulationApi:
    """Aplicación de prueba y fábrica de sesiones de su base temporal."""

    app: FastAPI
    session_factory: sessionmaker[Session]


@pytest.fixture
def simulation_api(migrated_database: Path) -> Iterator[SimulationApi]:
    """Crea la API con una base SQLite temporal migrada con Alembic."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)
    app = create_app()

    def _customer_dependency() -> Iterator[CreateCustomer]:
        with session_factory() as session:
            yield build_customer_use_case(session)

    def _simulation_dependency() -> Iterator[CreateSimulation]:
        with session_factory() as session:
            yield build_simulation_use_case(session)

    app.dependency_overrides[get_create_customer_use_case] = _customer_dependency
    app.dependency_overrides[get_create_simulation_use_case] = _simulation_dependency

    try:
        yield SimulationApi(app=app, session_factory=session_factory)
    finally:
        engine.dispose()


def _customer(*, tax_id: str = "B12345674") -> Customer:
    return Customer(
        id=uuid4(),
        legal_name="Cliente de simulación",
        tax_id=SpanishTaxId.parse(tax_id),
        email="cliente@example.com",
        country=CountryCode.ES,
        plan=PlanCode.STANDARD,
        created_at=datetime.now(UTC),
    )


def _create_customer(simulation_api: SimulationApi) -> Customer:
    customer = _customer()
    with simulation_api.session_factory() as session:
        SqlAlchemyCustomerRepository(session).add(customer)
    return customer


def _payload(customer_id: UUID, user_count: object = 100) -> dict[str, object]:
    return {"customer_id": str(customer_id), "user_count": user_count}


async def _post(
    app: FastAPI,
    payload: dict[str, object] | None = None,
    *,
    raise_app_exceptions: bool = True,
) -> Response:
    transport = ASGITransport(app=app, raise_app_exceptions=raise_app_exceptions)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.post("/simulations", json=payload)


async def _get(app: FastAPI, path: str) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.get(path)


def _stored_simulations(simulation_api: SimulationApi) -> list[SimulationModel]:
    with simulation_api.session_factory() as session:
        return list(session.scalars(select(SimulationModel)).all())


def test_create_simulation_returns_201_and_persists_the_contract(
    simulation_api: SimulationApi,
) -> None:
    """La creación devuelve 201, sin Location y con el contrato aprobado."""

    customer = _create_customer(simulation_api)

    response = asyncio.run(_post(simulation_api.app, _payload(customer.id)))

    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert "location" not in response.headers

    body = response.json()
    assert UUID(body["id"])
    assert body["customer_id"] == str(customer.id)
    assert body["user_count"] == 100
    assert body["user_subtotal_eur"] == "670.00"
    assert isinstance(body["user_subtotal_eur"], str)
    assert body["created_at"].endswith("Z")

    stored = _stored_simulations(simulation_api)
    assert len(stored) == 1
    assert str(stored[0].id) == body["id"]
    assert stored[0].customer_id == customer.id
    assert stored[0].user_count == 100
    assert stored[0].user_subtotal_eur == "670.00"


@pytest.mark.parametrize(
    ("user_count", "expected"),
    [
        (1, "10.00"),
        (10, "100.00"),
        (11, "108.00"),
        (50, "420.00"),
        (51, "425.00"),
        (100, "670.00"),
        (1_000_000, "5000170.00"),
    ],
)
def test_create_simulation_returns_the_approved_subtotals(
    simulation_api: SimulationApi,
    user_count: int,
    expected: str,
) -> None:
    """Los siete ejemplos comerciales se serializan como cadenas exactas."""

    customer = _create_customer(simulation_api)

    response = asyncio.run(_post(simulation_api.app, _payload(customer.id, user_count)))

    assert response.status_code == 201
    assert response.json()["user_subtotal_eur"] == expected
    assert _stored_simulations(simulation_api)[0].user_subtotal_eur == expected


@pytest.mark.parametrize(
    "user_count",
    [0, -1, 1_000_001, 10**100, 10.0, 10.5, "10", True, False, None],
)
def test_invalid_user_count_returns_problem_422_and_does_not_persist(
    simulation_api: SimulationApi,
    user_count: object,
) -> None:
    """La API rechaza entradas no estrictas o fuera del rango."""

    customer = _create_customer(simulation_api)

    response = asyncio.run(_post(simulation_api.app, _payload(customer.id, user_count)))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["title"] == "Datos de simulación no válidos"
    assert _stored_simulations(simulation_api) == []


@pytest.mark.parametrize("field", ["customer_id", "user_count"])
def test_missing_required_field_returns_problem_422(
    simulation_api: SimulationApi,
    field: str,
) -> None:
    """La ausencia de un campo obligatorio devuelve 422."""

    customer = _create_customer(simulation_api)
    payload = _payload(customer.id)
    payload.pop(field)

    response = asyncio.run(_post(simulation_api.app, payload))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert any(error["field"] == f"body.{field}" for error in response.json()["errors"])
    assert _stored_simulations(simulation_api) == []


def test_malformed_customer_id_returns_problem_422(
    simulation_api: SimulationApi,
) -> None:
    """Un UUID malformado es entrada inválida, no cliente inexistente."""

    response = asyncio.run(
        _post(
            simulation_api.app,
            {"customer_id": "no-es-un-uuid", "user_count": 100},
        )
    )

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["title"] == "Datos de simulación no válidos"
    assert _stored_simulations(simulation_api) == []


def test_unknown_customer_returns_problem_404_and_does_not_persist(
    simulation_api: SimulationApi,
) -> None:
    """Un UUID válido no registrado devuelve 404 problem+json."""

    response = asyncio.run(_post(simulation_api.app, _payload(uuid4())))

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["title"] == "Cliente no encontrado"
    assert _stored_simulations(simulation_api) == []


def test_unexpected_error_returns_problem_500_without_internal_details(
    simulation_api: SimulationApi,
) -> None:
    """Un fallo interno devuelve 500 sin filtrar el mensaje original."""

    def _broken_dependency() -> CreateSimulation:
        raise RuntimeError("detalle interno que no debe filtrarse")

    simulation_api.app.dependency_overrides[get_create_simulation_use_case] = _broken_dependency

    response = asyncio.run(
        _post(
            simulation_api.app,
            _payload(uuid4()),
            raise_app_exceptions=False,
        )
    )

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "detalle interno" not in response.text
    assert "traceback" not in response.text.lower()


def test_openapi_documents_the_simulation_contract(
    simulation_api: SimulationApi,
) -> None:
    """OpenAPI documenta ruta, esquemas y respuestas de error."""

    response = asyncio.run(_get(simulation_api.app, "/openapi.json"))

    assert response.status_code == 200
    payload = response.json()
    operation = payload["paths"]["/simulations"]["post"]
    assert operation["responses"]["201"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/SimulationResponse"
    )
    for status_code in ("404", "422", "500"):
        assert "application/problem+json" in operation["responses"][status_code]["content"]

    schemas = payload["components"]["schemas"]
    assert "SimulationCreateRequest" in schemas
    assert "SimulationResponse" in schemas
    assert schemas["SimulationCreateRequest"]["properties"]["user_count"]["minimum"] == 1
    assert schemas["SimulationCreateRequest"]["properties"]["user_count"]["maximum"] == 1_000_000
