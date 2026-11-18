"""Pruebas de la API HTTP de creación de simulaciones."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from urllib.error import URLError
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.application.simulations.estimator import MonthlyEstimator
from saas_o_matic.application.simulations.use_cases import CreateSimulation
from saas_o_matic.bootstrap.customers import build_customer_use_case
from saas_o_matic.bootstrap.simulations import build_simulation_use_case
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    PlanCode,
    SpanishTaxId,
)
from saas_o_matic.domain.simulations.calculation import MonthlyCalculation
from saas_o_matic.infrastructure.customers.repositories import (
    SqlAlchemyCustomerRepository,
)
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)
from saas_o_matic.infrastructure.frankfurter import FrankfurterRates
from saas_o_matic.infrastructure.simulations.models import SimulationModel
from saas_o_matic.infrastructure.simulations.repositories import SqlAlchemySimulationRepository
from saas_o_matic.infrastructure.tax_catalog import configured_tax_catalog
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
    return {
        "customer_id": str(customer_id),
        "user_count": user_count,
        "storage_gb": 250,
        "api_calls_per_month": 100000,
    }


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
    assert body["storage_gb"] == 250
    assert body["api_calls_per_month"] == 100000
    assert body["billing_period"] == "monthly"

    stored = _stored_simulations(simulation_api)
    assert len(stored) == 1
    assert str(stored[0].id) == body["id"]
    assert stored[0].customer_id == customer.id
    assert stored[0].user_count == 100
    assert stored[0].user_subtotal_eur == "670.00"
    assert stored[0].storage_gb == 250
    assert stored[0].api_calls_per_month == 100000
    assert stored[0].billing_period == "monthly"


@pytest.mark.parametrize(
    ("user_count", "expected"),
    [
        (0, "0.00"),
        (15, "140.00"),
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
    """Los nueve ejemplos comerciales se serializan como cadenas exactas."""

    customer = _create_customer(simulation_api)

    response = asyncio.run(_post(simulation_api.app, _payload(customer.id, user_count)))

    assert response.status_code == 201
    assert response.json()["user_subtotal_eur"] == expected
    assert _stored_simulations(simulation_api)[0].user_subtotal_eur == expected


@pytest.mark.parametrize(
    "user_count",
    [-1, 1_000_001, 10**100, 10.0, 10.5, "10", True, False, None],
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


@pytest.mark.parametrize(
    "field", ["customer_id", "user_count", "storage_gb", "api_calls_per_month"]
)
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
            {**_payload(uuid4()), "customer_id": "no-es-un-uuid"},
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
    assert schemas["SimulationCreateRequest"]["properties"]["user_count"]["minimum"] == 0
    assert schemas["SimulationCreateRequest"]["properties"]["user_count"]["maximum"] == 1_000_000
    assert schemas["SimulationCreateRequest"]["additionalProperties"] is False


@pytest.mark.parametrize(
    "field,maximum", [("storage_gb", 1000000), ("api_calls_per_month", 1000000000)]
)
@pytest.mark.parametrize("value", [-1, True, False, 1.0, 1.5, "1", None, 1000000001])
def test_consumption_invalid_never_persists(
    simulation_api: SimulationApi,
    field: str,
    maximum: int,
    value: object,
) -> None:
    """Los consumos son enteros estrictos y los rechazos no dejan filas parciales."""

    customer = _create_customer(simulation_api)
    if value == 1000000001:
        value = maximum + 1
    response = asyncio.run(_post(simulation_api.app, {**_payload(customer.id), field: value}))
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_simulations(simulation_api) == []


@pytest.mark.parametrize("value", [0, 1000000])
def test_consumption_boundaries_do_not_change_pricing(
    simulation_api: SimulationApi, value: int
) -> None:
    customer = _create_customer(simulation_api)
    payload = {
        **_payload(customer.id, 15),
        "storage_gb": value,
        "api_calls_per_month": value * 1000,
    }
    response = asyncio.run(_post(simulation_api.app, payload))
    assert response.status_code == 201
    assert response.json()["user_subtotal_eur"] == "140.00"
    assert response.json()["storage_gb"] == value
    assert response.json()["api_calls_per_month"] == value * 1000


@pytest.mark.parametrize("field", ["billing_period", "plan", "tax_rate", "currency", "unknown"])
def test_unknown_fields_are_problem_422(simulation_api: SimulationApi, field: str) -> None:
    customer = _create_customer(simulation_api)
    response = asyncio.run(_post(simulation_api.app, {**_payload(customer.id), field: "monthly"}))
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_simulations(simulation_api) == []


def _configure_fx(simulation_api: SimulationApi, *, unavailable: bool = False) -> list[str]:
    calls: list[str] = []

    def request(url: str, timeout: float) -> bytes:
        calls.append(url)
        if unavailable:
            raise URLError("offline")
        quote = "GBP" if url.endswith("GBP") else "USD"
        return (
            '{"base":"EUR","quote":"' + quote + '","date":"2026-11-16","rate":1.080000000000000001}'
        ).encode()

    estimator = MonthlyEstimator(
        configured_tax_catalog(),
        FrankfurterRates(request=request, now=lambda: datetime(2026, 11, 17, tzinfo=UTC)),
    )

    def dependency() -> Iterator[CreateSimulation]:
        with simulation_api.session_factory() as session:
            yield build_simulation_use_case(session, estimator)

    simulation_api.app.dependency_overrides[get_create_simulation_use_case] = dependency
    return calls


@pytest.mark.parametrize("currency", [None, "EUR", "USD", "GBP"])
def test_full_calculation_contract_and_physical_snapshot(
    simulation_api: SimulationApi,
    currency: str | None,
) -> None:
    calls = _configure_fx(simulation_api)
    customer = _create_customer(simulation_api)
    payload = _payload(customer.id, 15)
    if currency is not None:
        payload["display_currency"] = currency
    response = asyncio.run(_post(simulation_api.app, payload))
    assert response.status_code == 201
    body = response.json()
    assert body["tax_country"] == "ES"
    assert body["tax_rate"] == "0.21"
    assert body["tax_amount_eur"] == "29.40"
    assert body["total_eur"] == "169.40"
    assert body["tax_effective_from"] is None
    assert body["tax_verified_on"] == "2026-11-17"
    assert body["tax_source"].startswith("https://")
    assert body["tax_catalog_version"] == "general-vat-2026-11-17-v1"
    if currency in (None, "EUR"):
        assert calls == []
        assert body["converted_total"] == "169.40"
        assert body["exchange_rate_date"] is None
        assert body["exchange_rate_source"] == "identity"
    else:
        assert len(calls) == 1
        assert body["converted_total"] == "182.95"
        assert body["exchange_rate"] == "1.080000000000000001"
        assert body["exchange_rate_date"] == "2026-11-16"
        assert body["exchange_rate_source"] == "frankfurter"
    assert body["exchange_rate_obtained_at"].endswith("Z")
    with simulation_api.session_factory() as session:
        row = session.execute(
            text(
                "SELECT typeof(user_subtotal_eur), typeof(calculation_snapshot), "
                "calculation_snapshot "
                "FROM simulations"
            )
        ).one()
        assert row[0] == row[1] == "text"
        snapshot = json.loads(row[2])
        for key in ("tax_rate", "tax_amount_eur", "total_eur", "exchange_rate", "converted_total"):
            assert isinstance(snapshot[key], str)
        restored = SqlAlchemySimulationRepository(session).get_by_id(UUID(body["id"]))
        assert restored is not None and restored.calculation is not None
        assert restored.user_subtotal_eur == Decimal("140.00")
        assert restored.created_at.tzinfo is UTC
        assert restored.calculation.total_eur == Decimal("169.40")
        restored.calculation.validate_against(restored.user_subtotal_eur)
        # Reconstruir no usa el catálogo actual ni vuelve a consultar el proveedor.
        assert MonthlyCalculation.restore(snapshot) == restored.calculation


def test_fx_unavailable_no_partial_and_eur_still_operational(simulation_api: SimulationApi) -> None:
    calls = _configure_fx(simulation_api, unavailable=True)
    customer = _create_customer(simulation_api)
    response = asyncio.run(
        _post(
            simulation_api.app,
            {
                **_payload(customer.id, 15),
                "display_currency": "USD",
            },
        )
    )
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "offline" not in response.text
    assert _stored_simulations(simulation_api) == []
    eur = asyncio.run(_post(simulation_api.app, _payload(customer.id, 15)))
    assert eur.status_code == 201
    assert eur.json()["total_eur"] == "169.40"
    assert len(calls) == 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("display_currency", "JPY"),
        ("display_currency", None),
        ("tax_country", "PT"),
        ("tax_rate", "0.01"),
        ("exchange_rate", "100"),
        ("tax_amount_eur", "0.00"),
        ("total_eur", "1.00"),
        ("converted_total", "1.00"),
    ],
)
def test_manipulated_calculation_is_rejected(
    simulation_api: SimulationApi,
    field: str,
    value: object,
) -> None:
    customer = _create_customer(simulation_api)
    response = asyncio.run(_post(simulation_api.app, {**_payload(customer.id), field: value}))
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_simulations(simulation_api) == []


def test_no_read_transaction_held_during_provider(simulation_api: SimulationApi) -> None:
    customer = _create_customer(simulation_api)
    with simulation_api.session_factory() as session:

        def request(url: str, timeout: float) -> bytes:
            assert not session.in_transaction()
            return b'{"base":"EUR","quote":"USD","rate":1.08,"date":"2026-11-16"}'

        estimator = MonthlyEstimator(
            configured_tax_catalog(),
            FrankfurterRates(request=request, now=lambda: datetime(2026, 11, 17, tzinfo=UTC)),
        )
        from saas_o_matic.application.simulations.dto import CreateSimulationCommand, Currency

        result = build_simulation_use_case(session, estimator).execute(
            CreateSimulationCommand(customer.id, 15, 250, 100000, Currency.USD)
        )
        assert result.calculation["total_eur"] == "169.40"


@pytest.mark.parametrize(
    "country,total",
    [
        ("ES", "169.40"),
        ("PT", "172.20"),
        ("FR", "168.00"),
        ("DE", "166.60"),
        ("IT", "170.80"),
        ("NL", "169.40"),
    ],
)
def test_tax_country_is_read_from_registered_customer(
    simulation_api: SimulationApi,
    country: str,
    total: str,
) -> None:
    customer = _create_customer(simulation_api)
    with simulation_api.session_factory() as session:
        session.execute(text("UPDATE customers SET country=:country"), {"country": country})
        session.commit()
    response = asyncio.run(_post(simulation_api.app, _payload(customer.id, 15)))
    assert response.status_code == 201
    assert response.json()["tax_country"] == country
    assert response.json()["total_eur"] == total
