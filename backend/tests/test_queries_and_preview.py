"""Consultas y preview integrados con SQLite real temporal y proveedor falso."""

from __future__ import annotations

import asyncio
import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib.error import URLError
from uuid import UUID

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import event, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.queries import CustomerQueries
from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.application.simulations.estimator import MonthlyEstimator
from saas_o_matic.application.simulations.queries import SimulationQueries
from saas_o_matic.application.simulations.use_cases import CreateSimulation, PreviewSimulation
from saas_o_matic.bootstrap.customers import build_customer_queries, build_customer_use_case
from saas_o_matic.bootstrap.simulations import (
    build_preview_use_case,
    build_simulation_queries,
    build_simulation_use_case,
)
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import CountryCode, PlanCode, parse_tax_id
from saas_o_matic.domain.simulations.calculation import (
    Currency,
    ExchangeQuote,
    TaxCatalog,
    calculate_monthly,
)
from saas_o_matic.domain.simulations.entities import Simulation
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository
from saas_o_matic.infrastructure.database import create_session_factory, create_sqlite_engine
from saas_o_matic.infrastructure.frankfurter import FrankfurterRates
from saas_o_matic.infrastructure.simulations.models import SimulationModel
from saas_o_matic.infrastructure.simulations.repositories import SqlAlchemySimulationRepository
from saas_o_matic.infrastructure.tax_catalog import configured_tax_catalog
from saas_o_matic.presentation.app import create_app
from saas_o_matic.presentation.customers.dependencies import (
    get_create_customer_use_case,
    get_customer_queries,
)
from saas_o_matic.presentation.simulations.dependencies import (
    get_create_simulation_use_case,
    get_preview_simulation_use_case,
    get_simulation_queries,
)


@dataclass
class FakeRates:
    fail: bool = False
    calls: int = 0
    body: bytes | None = None

    def request(self, url: str, timeout: float) -> bytes:
        self.calls += 1
        assert timeout == 5
        if self.fail:
            raise URLError("Fallo de red simulado, no debe filtrarse")
        if self.body is not None:
            return self.body
        quote = "GBP" if url.endswith("GBP") else "USD"
        return ('{"date":"2026-11-17","base":"EUR","quote":"' + quote + '","rate":1.08}').encode()


@dataclass
class QueryApi:
    app: FastAPI
    engine: Engine
    sessions: sessionmaker[Session]
    rates: FakeRates
    estimator: MonthlyEstimator


@pytest.fixture
def query_api(migrated_database: Path) -> Iterator[QueryApi]:
    engine = create_sqlite_engine(migrated_database)
    sessions = create_session_factory(engine)
    rates = FakeRates()
    estimator = MonthlyEstimator(
        configured_tax_catalog(),
        FrankfurterRates(
            request=rates.request,
            now=lambda: datetime(2026, 11, 18, tzinfo=UTC),
        ),
    )
    app = create_app()

    def create_customer() -> Iterator[CreateCustomer]:
        with sessions() as session:
            yield build_customer_use_case(session)

    def customers() -> Iterator[CustomerQueries]:
        with sessions() as session:
            yield build_customer_queries(session)

    def simulations() -> Iterator[SimulationQueries]:
        with sessions() as session:
            yield build_simulation_queries(session)

    def create_simulation() -> Iterator[CreateSimulation]:
        with sessions() as session:
            yield build_simulation_use_case(session, estimator)

    def preview() -> Iterator[PreviewSimulation]:
        with sessions() as session:
            yield build_preview_use_case(session, estimator)

    app.dependency_overrides.update(
        {
            get_create_customer_use_case: create_customer,
            get_customer_queries: customers,
            get_simulation_queries: simulations,
            get_create_simulation_use_case: create_simulation,
            get_preview_simulation_use_case: preview,
        }
    )
    try:
        yield QueryApi(app, engine, sessions, rates, estimator)
    finally:
        engine.dispose()


def request(
    api: QueryApi, method: str, path: str, payload: dict[str, object] | None = None
) -> Response:
    async def send() -> Response:
        async with AsyncClient(
            transport=ASGITransport(app=api.app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, json=payload)

    return asyncio.run(send())


def seed_customer(
    api: QueryApi,
    number: int = 1,
    name: str = "École ACME",
    country: str = "FR",
    tax_id: str | None = None,
) -> Customer:
    code = CountryCode(country)
    customer = Customer(
        id=UUID(int=number),
        legal_name=name,
        tax_id=parse_tax_id(tax_id or ("12345678Z" if country == "ES" else f"ID-{number}"), code),
        country=code,
        email="contact@example.com",
        plan=PlanCode.STANDARD,
        created_at=datetime(2026, 11, 17, tzinfo=UTC),
    )
    with api.sessions() as session:
        SqlAlchemyCustomerRepository(session).add(customer)
    return customer


def payload(customer: Customer, **changes: object) -> dict[str, object]:
    return {
        "customer_id": str(customer.id),
        "user_count": 15,
        "storage_gb": 250,
        "api_calls_per_month": 100000,
        **changes,
    }


def test_empty_list_default_pagination(query_api: QueryApi) -> None:
    response = request(query_api, "GET", "/customers")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0, "limit": 20, "offset": 0}


@pytest.mark.parametrize(
    "search", ["acme", "ACME", "ÉCOLE", "école", "ID-1", "id-1", "%20acme%20", "", "%20%20"]
)
def test_partial_unicode_search_and_whitespace(query_api: QueryApi, search: str) -> None:
    customer = seed_customer(query_api)
    response = request(query_api, "GET", f"/customers?search={search}")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == str(customer.id)
    assert body["items"][0]["created_at"].endswith("Z")


@pytest.mark.parametrize(
    "name,search,expected",
    [
        ("Über", "ÜBER", 1),
        ("Straße", "STRASSE", 1),
        ("École", "ecole", 0),
        ("École", "E\u0301cole", 0),
    ],
)
def test_documented_unicode_semantics(
    query_api: QueryApi, name: str, search: str, expected: int
) -> None:
    from urllib.parse import urlencode

    seed_customer(query_api, name=name)
    response = request(query_api, "GET", "/customers?" + urlencode({"search": search}))
    assert response.status_code == 200
    assert response.json()["total"] == expected


@pytest.mark.parametrize("literal", ["%", "_", "\\", "%' OR 1=1 --"])
def test_like_literals_and_sql_looking_input(query_api: QueryApi, literal: str) -> None:
    from urllib.parse import urlencode

    match = seed_customer(query_api, 1, "Literal " + literal)
    seed_customer(query_api, 2, "Normal")
    response = request(query_api, "GET", "/customers?" + urlencode({"search": literal}))
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == str(match.id)


def test_or_search_has_no_duplicate_rows(query_api: QueryApi) -> None:
    seed_customer(query_api, name="ACME", tax_id="ACME-123")
    assert request(query_api, "GET", "/customers?search=acme").json()["total"] == 1
    assert request(query_api, "GET", "/customers?search=missing").json()["items"] == []


def test_deterministic_order_and_total_before_pagination(query_api: QueryApi) -> None:
    seed_customer(query_api, 3, "beta")
    seed_customer(query_api, 2, "ACME")
    seed_customer(query_api, 1, "acme")
    first = request(query_api, "GET", "/customers?limit=1&offset=0").json()
    second = request(query_api, "GET", "/customers?limit=1&offset=1").json()
    assert first["items"][0]["id"] == str(UUID(int=1))
    assert second["items"][0]["id"] == str(UUID(int=2))
    assert first["total"] == second["total"] == 3
    assert request(query_api, "GET", "/customers?limit=1&offset=0").json() == first
    for offset in (3, 10**30):
        page = request(query_api, "GET", f"/customers?limit=100&offset={offset}")
        assert page.status_code == 200
        assert page.json() == {"items": [], "total": 3, "limit": 100, "offset": offset}


@pytest.mark.parametrize(
    "query",
    [
        "limit=0",
        "limit=101",
        "limit=-1",
        "limit=1.5",
        "limit=x",
        "offset=-1",
        "offset=1.5",
        "offset=x",
        "search=" + "x" * 256,
    ],
)
def test_invalid_query_problem_422(query_api: QueryApi, query: str) -> None:
    response = request(query_api, "GET", "/customers?" + query)
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")


def test_search_length_applies_after_trim(query_api: QueryApi) -> None:
    response = request(query_api, "GET", "/customers?search=" + "%20" * 10 + "x" * 255 + "%20" * 10)
    assert response.status_code == 200


@pytest.mark.parametrize("country", ["ES", "PT", "FR", "DE", "IT", "NL"])
def test_detail_coherent_with_registered_customer(query_api: QueryApi, country: str) -> None:
    creation = request(
        query_api,
        "POST",
        "/customers",
        {
            "legal_name": "Cliente internacional",
            "tax_id": "12345678Z",
            "email": "test@example.com",
            "country": country,
            "plan": "standard",
        },
    )
    assert creation.status_code == 201
    detail = request(query_api, "GET", "/customers/" + creation.json()["id"])
    assert detail.status_code == 200
    assert detail.json() == creation.json()


@pytest.mark.parametrize("suffix", ["", "/simulations"])
@pytest.mark.parametrize("identifier,status", [(str(UUID(int=999)), 404), ("invalid-uuid", 422)])
def test_detail_history_unknown_or_invalid_id(
    query_api: QueryApi, suffix: str, identifier: str, status: int
) -> None:
    response = request(query_api, "GET", f"/customers/{identifier}{suffix}")
    assert response.status_code == status
    assert response.headers["content-type"].startswith("application/problem+json")


def test_customer_with_no_simulations(query_api: QueryApi) -> None:
    customer = seed_customer(query_api)
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").json() == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def seed_simulation(
    api: QueryApi, customer: Customer, number: int, generation: int = 37, days: int = 0
) -> None:
    calculation = None
    if generation == 37:
        calculation = calculate_monthly(
            Decimal("140.00"),
            configured_tax_catalog().for_country(customer.country),
            ExchangeQuote(
                Currency.USD,
                Decimal("1.080000000000000001"),
                datetime(2026, 11, 17).date(),
                datetime(2026, 11, 18, tzinfo=UTC),
                "frankfurter",
            ),
        )
    simulation = Simulation(
        id=UUID(int=number),
        customer_id=customer.id,
        user_count=15,
        user_subtotal_eur=Decimal("140.00"),
        created_at=datetime(2026, 11, 18, tzinfo=UTC) + timedelta(days=days),
        storage_gb=None if generation == 32 else 250,
        api_calls_per_month=None if generation == 32 else 100000,
        calculation=calculation,
    )
    with api.sessions() as session:
        SqlAlchemySimulationRepository(session).add(simulation)


def test_history_three_generations_and_no_current_references(
    query_api: QueryApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    customer = seed_customer(query_api, country="ES")
    for number, generation in ((1, 32), (2, 36), (3, 37)):
        seed_simulation(query_api, customer, number, generation)
    with query_api.sessions() as session:
        session.execute(text("UPDATE customers SET country='PT'"))
        session.commit()
    query_api.rates.fail = True

    def forbidden(*args: Any, **kwargs: Any) -> Any:
        pytest.fail("El historial no debe estimar ni cargar catálogo ni consultar divisas")

    monkeypatch.setattr(MonthlyEstimator, "estimate", forbidden)
    monkeypatch.setattr(FrankfurterRates, "get_rate", forbidden)
    monkeypatch.setattr(TaxCatalog, "for_country", forbidden)
    response = request(query_api, "GET", f"/customers/{customer.id}/simulations")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    complete, expanded, initial = body["items"]
    assert complete["id"] == str(UUID(int=3))
    assert complete["tax_country"] == "ES"
    assert complete["total_eur"] == "169.40"
    assert complete["exchange_rate"] == "1.080000000000000001"
    assert complete["converted_total"] == "182.95"
    assert complete["exchange_rate_obtained_at"].endswith("Z")
    for historical in (expanded, initial):
        assert historical["user_subtotal_eur"] == "140.00"
        assert historical["total_eur"] is None
        assert historical["display_currency"] is None
        for key in complete.keys() - {
            "id",
            "customer_id",
            "user_count",
            "storage_gb",
            "api_calls_per_month",
            "billing_period",
            "user_subtotal_eur",
            "created_at",
        }:
            assert historical[key] is None
        assert historical["created_at"].endswith("Z")
    assert initial["storage_gb"] is initial["api_calls_per_month"] is None
    assert expanded["storage_gb"] == 250
    assert expanded["api_calls_per_month"] == 100000
    assert query_api.rates.calls == 0


def test_history_customer_isolation_order_pagination(query_api: QueryApi) -> None:
    customer = seed_customer(query_api, 1)
    other = seed_customer(query_api, 2)
    seed_simulation(query_api, customer, 1, days=0)
    seed_simulation(query_api, customer, 2, days=1)
    seed_simulation(query_api, customer, 3, days=1)
    seed_simulation(query_api, other, 4, days=2)
    path = f"/customers/{customer.id}/simulations"
    first = request(query_api, "GET", path + "?limit=1&offset=0").json()
    second = request(query_api, "GET", path + "?limit=1&offset=1").json()
    assert first["items"][0]["id"] == str(UUID(int=3))
    assert second["items"][0]["id"] == str(UUID(int=2))
    assert first["total"] == second["total"] == 3
    empty = request(query_api, "GET", path + f"?limit=100&offset={10**30}")
    assert empty.status_code == 200
    assert empty.json() == {"items": [], "total": 3, "limit": 100, "offset": 10**30}


@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1", "offset=x"])
def test_history_invalid_pagination(query_api: QueryApi, query: str) -> None:
    customer = seed_customer(query_api)
    response = request(query_api, "GET", f"/customers/{customer.id}/simulations?{query}")
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")


@pytest.mark.parametrize(
    ("column", "corrupt_value"),
    [
        ("calculation_snapshot", '{"schema_version":"1"}'),
        ("user_subtotal_eur", "not-a-decimal"),
    ],
)
def test_corrupt_history_row_is_a_controlled_500_without_changes(
    query_api: QueryApi,
    column: str,
    corrupt_value: str,
) -> None:
    customer = seed_customer(query_api, country="ES")
    seed_simulation(query_api, customer, 1)
    seed_simulation(query_api, customer, 2)
    with query_api.sessions() as session:
        session.execute(
            text(f"UPDATE simulations SET {column}=:value WHERE id=:identifier"),
            {"value": corrupt_value, "identifier": UUID(int=2).hex},
        )
        session.commit()
    with query_api.engine.connect() as connection:
        before = connection.execute(text("SELECT * FROM simulations ORDER BY id")).all()

    response = request(query_api, "GET", f"/customers/{customer.id}/simulations")

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "schema_version" not in response.text
    assert "not-a-decimal" not in response.text
    assert "Traceback" not in response.text
    with query_api.engine.connect() as connection:
        after = connection.execute(text("SELECT * FROM simulations ORDER BY id")).all()
    assert after == before


@pytest.mark.parametrize(
    "users,subtotal",
    [
        (0, "0.00"),
        (1, "10.00"),
        (10, "100.00"),
        (11, "108.00"),
        (15, "140.00"),
        (50, "420.00"),
        (51, "425.00"),
        (100, "670.00"),
        (1000000, "5000170.00"),
    ],
)
def test_preview_pricing_without_persistence(
    query_api: QueryApi, users: int, subtotal: str
) -> None:
    customer = seed_customer(query_api, country="ES")
    response = request(
        query_api, "POST", "/simulations/preview", payload(customer, user_count=users)
    )
    assert response.status_code == 200
    assert response.json()["user_subtotal_eur"] == subtotal
    assert response.json()["exchange_rate_source"] == "identity"
    assert response.json()["exchange_rate_date"] is None
    assert "id" not in response.json() and "created_at" not in response.json()
    assert "location" not in response.headers
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").json()["total"] == 0


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
def test_preview_six_countries(query_api: QueryApi, country: str, total: str) -> None:
    customer = seed_customer(query_api, country=country)
    response = request(query_api, "POST", "/simulations/preview", payload(customer))
    assert response.status_code == 200
    assert response.json()["tax_country"] == country
    assert response.json()["total_eur"] == total


@pytest.mark.parametrize("currency", ["EUR", "USD", "GBP"])
def test_preview_save_parity_and_shared_cache(query_api: QueryApi, currency: str) -> None:
    customer = seed_customer(query_api, country="ES")
    body = payload(customer, display_currency=currency)
    previews = [request(query_api, "POST", "/simulations/preview", body).json() for _ in range(3)]
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").json()["total"] == 0
    saved = request(query_api, "POST", "/simulations", body)
    assert saved.status_code == 201
    persisted = saved.json()
    for preview in previews:
        assert preview == {
            key: value
            for key, value in persisted.items()
            if key not in {"id", "created_at", "exchange_rate_obtained_at"}
        } | {
            "exchange_rate_obtained_at": preview["exchange_rate_obtained_at"],
        }
    assert query_api.rates.calls == (0 if currency == "EUR" else 1)
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").json()["items"] == [
        persisted
    ]


@pytest.mark.parametrize(
    "field,value",
    [
        ("user_count", -1),
        ("user_count", True),
        ("user_count", 1.5),
        ("user_count", "15"),
        ("user_count", 1000001),
        ("storage_gb", None),
        ("storage_gb", 1000001),
        ("api_calls_per_month", True),
        ("api_calls_per_month", 1000000001),
        ("display_currency", "JPY"),
        ("tax_rate", "0.00"),
        ("total_eur", "0.00"),
        ("exchange_rate", "100"),
        ("tax_country", "PT"),
        ("billing_period", "monthly"),
        ("unknown", 123),
    ],
)
def test_preview_invalid_or_manipulated(query_api: QueryApi, field: str, value: object) -> None:
    customer = seed_customer(query_api)
    response = request(
        query_api, "POST", "/simulations/preview", payload(customer, **{field: value})
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")


@pytest.mark.parametrize(
    "field", ["customer_id", "user_count", "storage_gb", "api_calls_per_month"]
)
def test_preview_missing_field(query_api: QueryApi, field: str) -> None:
    body = payload(seed_customer(query_api))
    body.pop(field)
    response = request(query_api, "POST", "/simulations/preview", body)
    assert response.status_code == 422


def test_preview_unknown_customer_before_fx(query_api: QueryApi) -> None:
    response = request(
        query_api,
        "POST",
        "/simulations/preview",
        {
            "customer_id": str(UUID(int=999)),
            "user_count": 15,
            "storage_gb": 0,
            "api_calls_per_month": 0,
            "display_currency": "USD",
        },
    )
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert query_api.rates.calls == 0


def test_preview_503_and_eur_operational(query_api: QueryApi) -> None:
    customer = seed_customer(query_api)
    query_api.rates.fail = True
    response = request(
        query_api, "POST", "/simulations/preview", payload(customer, display_currency="USD")
    )
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "Fallo de red" not in response.text
    assert request(query_api, "POST", "/simulations/preview", payload(customer)).status_code == 200
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").json()["total"] == 0


@pytest.mark.parametrize(
    "body",
    [
        b'{"date":"2026-11-17","base":"EUR","quote":"USD","rate":1e999999}',
        b'{"date":"2026-11-17","base":"EUR","quote":"USD","rate":1.12345678901234567890123456789012}',
    ],
)
def test_pathological_external_rate_is_503_without_persistence(
    query_api: QueryApi,
    body: bytes,
) -> None:
    customer = seed_customer(query_api, country="ES")
    query_api.rates.body = body

    for path in ("/simulations/preview", "/simulations"):
        response = request(
            query_api,
            "POST",
            path,
            payload(customer, display_currency="USD"),
        )
        assert response.status_code == 503
        assert response.headers["content-type"].startswith("application/problem+json")
        assert "rango técnico" not in response.text
        assert "precisión no admitida" not in response.text

    history_path = f"/customers/{customer.id}/simulations"
    assert request(query_api, "GET", history_path).json()["total"] == 0

    query_api.rates.body = None
    recovered = request(
        query_api, "POST", "/simulations/preview", payload(customer, display_currency="USD")
    )
    assert recovered.status_code == 200
    assert recovered.json()["converted_total"] == "182.95"

    eur = request(query_api, "POST", "/simulations", payload(customer))
    assert eur.status_code == 201
    assert request(query_api, "GET", history_path).json()["total"] == 1


def test_preview_sqlite_authorizer_proves_no_writes(query_api: QueryApi) -> None:
    customer = seed_customer(query_api)
    denied: list[int] = []

    def authorize(
        action: int, arg1: str | None, arg2: str | None, db: str | None, trigger: str | None
    ) -> int:
        if action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE):
            denied.append(action)
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    def readonly_connection(connection: Any, record: Any) -> None:
        connection.set_authorizer(authorize)

    query_api.engine.dispose()
    event.listen(query_api.engine, "connect", readonly_connection)
    with pytest.raises(DatabaseError), query_api.engine.begin() as connection:
        connection.execute(text("UPDATE customers SET legal_name='blocked'"))
    assert denied
    denied.clear()
    for _ in range(3):
        response = request(
            query_api, "POST", "/simulations/preview", payload(customer, display_currency="USD")
        )
        assert response.status_code == 200
    assert denied == []
    with query_api.sessions() as session:
        assert session.scalars(select(SimulationModel)).all() == []
    assert query_api.rates.calls == 1


def test_complete_backend_flow(query_api: QueryApi) -> None:
    created = request(
        query_api,
        "POST",
        "/customers",
        {
            "legal_name": "ACME Backend",
            "tax_id": "12345678Z",
            "email": "test@example.com",
            "country": "ES",
            "plan": "standard",
        },
    )
    assert created.status_code == 201
    customer = created.json()
    assert request(query_api, "GET", "/customers?search=acme").json()["items"] == [customer]
    assert request(query_api, "GET", f"/customers/{customer['id']}").json() == customer
    body = {
        "customer_id": customer["id"],
        "user_count": 15,
        "storage_gb": 250,
        "api_calls_per_month": 100000,
    }
    preview = request(query_api, "POST", "/simulations/preview", body)
    assert preview.status_code == 200
    path = f"/customers/{customer['id']}/simulations"
    assert request(query_api, "GET", path).json()["total"] == 0
    saved = request(query_api, "POST", "/simulations", body)
    assert saved.status_code == 201
    history = request(query_api, "GET", path).json()
    assert history["total"] == 1
    assert history["items"] == [saved.json()]
    assert history["items"][0]["total_eur"] == preview.json()["total_eur"] == "169.40"


def test_read_query_count_is_bounded_no_n_plus_one(query_api: QueryApi) -> None:
    for number in range(1, 26):
        seed_customer(query_api, number, f"Cliente {number:02}")
    statements: list[str] = []

    def capture(*args: Any) -> None:
        statement = args[2]
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(query_api.engine, "before_cursor_execute", capture)
    body = request(query_api, "GET", "/customers?search=cliente").json()
    assert len(body["items"]) == 20 and body["total"] == 25
    assert len(statements) == 2
    assert "LIMIT" in statements[1].upper()
    assert "COUNT" in statements[0].upper()
    statements.clear()
    maximum = request(query_api, "GET", "/customers?limit=100").json()
    assert len(maximum["items"]) == 25 and maximum["limit"] == 100
    assert len(statements) == 2


def test_openapi_new_contracts(query_api: QueryApi) -> None:
    schema = request(query_api, "GET", "/openapi.json").json()
    paths = schema["paths"]
    for path in ("/customers", "/customers/{customer_id}", "/customers/{customer_id}/simulations"):
        assert "get" in paths[path]
        for code in ("422", "500"):
            assert "application/problem+json" in paths[path]["get"]["responses"][code]["content"]
    preview = paths["/simulations/preview"]["post"]
    assert "200" in preview["responses"]
    for code in ("404", "422", "503", "500"):
        assert "application/problem+json" in preview["responses"][code]["content"]
    request_schema = preview["requestBody"]["content"]["application/json"]["schema"]
    assert (
        request_schema
        == paths["/simulations"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    )
    schemas = schema["components"]["schemas"]
    properties = schemas["SimulationPreviewResponse"]["properties"]
    assert "id" not in properties and "created_at" not in properties
    assert properties["total_eur"]["type"] == "string"
    for name in (
        "storage_gb",
        "tax_rate",
        "total_eur",
        "display_currency",
        "exchange_rate_obtained_at",
    ):
        assert {
            part.get("type")
            for part in schemas["HistoricalSimulationResponse"]["properties"][name]["anyOf"]
        } >= {"null"}
    parameters = {p["name"]: p["schema"] for p in paths["/customers"]["get"]["parameters"]}
    assert parameters["limit"]["default"] == 20
    assert parameters["limit"]["minimum"] == 1 and parameters["limit"]["maximum"] == 100
    assert parameters["offset"]["minimum"] == 0
    assert any(s.get("maxLength") == 255 for s in parameters["search"]["anyOf"])


def test_unicode_function_exists_on_each_connection(query_api: QueryApi) -> None:
    with query_api.engine.connect() as first, query_api.engine.connect() as second:
        for connection in (first, second):
            assert (
                connection.execute(
                    text("SELECT unicode_casefold(:name)"), {"name": "ÉCOLE Straße"}
                ).scalar_one()
                == "école strasse"
            )


def test_history_uses_three_queries_not_one_per_record(query_api: QueryApi) -> None:
    customer = seed_customer(query_api)
    for number in range(1, 5):
        seed_simulation(query_api, customer, number)
    statements: list[str] = []

    def capture(*args: Any) -> None:
        if args[2].lstrip().upper().startswith("SELECT"):
            statements.append(args[2])

    event.listen(query_api.engine, "before_cursor_execute", capture)
    response = request(query_api, "GET", f"/customers/{customer.id}/simulations?limit=2")
    assert response.status_code == 200
    assert response.json()["total"] == 4
    assert len(response.json()["items"]) == 2
    assert len(statements) == 3
    assert "LIMIT" in statements[-1].upper()


def test_missing_customer_does_not_query_history_table(query_api: QueryApi) -> None:
    statements: list[str] = []

    def capture(*args: Any) -> None:
        statements.append(args[2])

    event.listen(query_api.engine, "before_cursor_execute", capture)
    response = request(query_api, "GET", f"/customers/{UUID(int=999)}/simulations")
    assert response.status_code == 404
    assert not any("FROM simulations" in statement for statement in statements)


@pytest.mark.parametrize("field", ["user_count", "storage_gb", "api_calls_per_month"])
@pytest.mark.parametrize("value", [None, False, 1.0, "1", -1])
def test_preview_numeric_fields_are_strict(query_api: QueryApi, field: str, value: object) -> None:
    customer = seed_customer(query_api)
    response = request(
        query_api, "POST", "/simulations/preview", payload(customer, **{field: value})
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")


@pytest.mark.parametrize(
    "path,method,dependency",
    [
        ("/customers", "GET", get_customer_queries),
        ("/customers/00000000-0000-0000-0000-000000000001", "GET", get_customer_queries),
        (
            "/customers/00000000-0000-0000-0000-000000000001/simulations",
            "GET",
            get_simulation_queries,
        ),
        ("/simulations/preview", "POST", get_preview_simulation_use_case),
    ],
)
def test_new_routes_unexpected_error_is_problem_500(
    query_api: QueryApi,
    path: str,
    method: str,
    dependency: Any,
) -> None:
    customer = seed_customer(query_api)

    def broken() -> Any:
        raise RuntimeError("Detalle interno que no debe filtrarse")

    query_api.app.dependency_overrides[dependency] = broken
    response = request(query_api, method, path, payload(customer) if method == "POST" else None)
    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "Detalle interno" not in response.text


def test_production_composition_wires_new_routes(
    query_api: QueryApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from saas_o_matic.bootstrap import main, simulations

    customer = seed_customer(query_api, country="ES")
    monkeypatch.setattr(main, "_get_session_factory", lambda: query_api.sessions)
    monkeypatch.setattr(simulations, "shared_estimator", lambda: query_api.estimator)
    query_api.app = main.app
    for dependency in (
        get_customer_queries,
        get_simulation_queries,
        get_preview_simulation_use_case,
    ):
        assert dependency in main.app.dependency_overrides
    assert request(query_api, "GET", "/customers").status_code == 200
    assert request(query_api, "GET", f"/customers/{customer.id}").status_code == 200
    assert request(query_api, "GET", f"/customers/{customer.id}/simulations").status_code == 200
    preview = request(
        query_api, "POST", "/simulations/preview", payload(customer, display_currency="USD")
    )
    assert preview.status_code == 200
    assert preview.json()["converted_total"] == "182.95"


def test_read_history_does_not_change_physical_rows(query_api: QueryApi) -> None:
    customer = seed_customer(query_api)
    for number, generation in ((1, 32), (2, 36), (3, 37)):
        seed_simulation(query_api, customer, number, generation)
    with query_api.engine.connect() as connection:
        before = connection.execute(text("SELECT * FROM simulations ORDER BY id")).all()
    for _ in range(2):
        assert request(query_api, "GET", f"/customers/{customer.id}/simulations").status_code == 200
    with query_api.engine.connect() as connection:
        after = connection.execute(text("SELECT * FROM simulations ORDER BY id")).all()
    assert before == after
