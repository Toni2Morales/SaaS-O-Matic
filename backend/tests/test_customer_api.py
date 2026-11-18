"""Pruebas de la API HTTP de alta de clientes."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from saas_o_matic.application.customers.catalogs import (
    LEGAL_NAME_MAX_LENGTH,
    LEGAL_NAME_MIN_LENGTH,
)
from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.bootstrap.customers import build_customer_use_case
from saas_o_matic.infrastructure.customers.models import CustomerModel
from saas_o_matic.infrastructure.database import (
    create_session_factory,
    create_sqlite_engine,
)
from saas_o_matic.presentation.app import create_app
from saas_o_matic.presentation.customers.dependencies import get_create_customer_use_case

VALID_TAX_ID = "B12345674"


@dataclass(frozen=True)
class CustomerApi:
    """Aplicación de prueba y fábrica de sesiones de su base temporal."""

    app: FastAPI
    session_factory: sessionmaker[Session]


@pytest.fixture
def customer_api(migrated_database: Path) -> Iterator[CustomerApi]:
    """Crea la API con una base SQLite temporal migrada con Alembic."""

    engine = create_sqlite_engine(migrated_database)
    session_factory = create_session_factory(engine)
    app = create_app()

    def _use_case_dependency() -> Iterator[CreateCustomer]:
        with session_factory() as session:
            yield build_customer_use_case(session)

    app.dependency_overrides[get_create_customer_use_case] = _use_case_dependency

    try:
        yield CustomerApi(app=app, session_factory=session_factory)
    finally:
        engine.dispose()


def _valid_payload() -> dict[str, object]:
    return {
        "legal_name": "Empresa Ejemplo S.L.",
        "tax_id": VALID_TAX_ID,
        "email": "contacto@ejemplo.es",
        "country": "ES",
        "plan": "standard",
    }


async def _post(
    app: FastAPI,
    payload: dict[str, object] | None = None,
    *,
    raw_body: str | None = None,
    raise_app_exceptions: bool = True,
) -> Response:
    transport = ASGITransport(app=app, raise_app_exceptions=raise_app_exceptions)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        if raw_body is not None:
            return await client.post(
                "/customers",
                content=raw_body,
                headers={"content-type": "application/json"},
            )
        return await client.post("/customers", json=payload)


async def _get(app: FastAPI, path: str) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.get(path)


def _stored_customers(customer_api: CustomerApi) -> list[CustomerModel]:
    with customer_api.session_factory() as session:
        return list(session.scalars(select(CustomerModel)).all())


def test_create_customer_returns_201_and_persists_the_client(
    customer_api: CustomerApi,
) -> None:
    """El alta devuelve 201 y el cliente queda persistido en SQLite."""

    response = asyncio.run(_post(customer_api.app, _valid_payload()))

    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert "location" not in response.headers

    body = response.json()
    assert UUID(body["id"])
    assert body["legal_name"] == "Empresa Ejemplo S.L."
    assert body["tax_id"] == VALID_TAX_ID
    assert body["email"] == "contacto@ejemplo.es"
    assert body["country"] == "ES"
    assert body["plan"] == "standard"
    created_at = datetime.fromisoformat(body["created_at"])
    assert created_at.tzinfo is not None

    with customer_api.session_factory() as session:
        model = session.scalar(select(CustomerModel).where(CustomerModel.tax_id == VALID_TAX_ID))
        assert model is not None
        assert str(model.id) == body["id"]
        assert model.legal_name == "Empresa Ejemplo S.L."
        assert model.plan == "standard"


def test_legal_name_is_trimmed_and_persisted(customer_api: CustomerApi) -> None:
    """La API recorta los espacios exteriores y conserva los interiores."""

    payload = _valid_payload()
    payload["legal_name"] = "  Empresa  Ejemplo S.L.  "

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 201
    assert response.json()["legal_name"] == "Empresa  Ejemplo S.L."
    stored = _stored_customers(customer_api)
    assert len(stored) == 1
    assert stored[0].legal_name == "Empresa  Ejemplo S.L."


@pytest.mark.parametrize("legal_name", ["", "   ", "\t\n"])
def test_blank_legal_name_returns_problem_422_and_does_not_persist(
    customer_api: CustomerApi,
    legal_name: str,
) -> None:
    """Una razón social vacía o solo con espacios se rechaza antes de persistir."""

    payload = _valid_payload()
    payload["legal_name"] = legal_name

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_customers(customer_api) == []


def test_legal_name_of_one_character_is_accepted(customer_api: CustomerApi) -> None:
    """El límite inferior se aplica después del recorte."""

    payload = _valid_payload()
    payload["legal_name"] = "A"

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 201
    assert response.json()["legal_name"] == "A"
    assert _stored_customers(customer_api)[0].legal_name == "A"


def test_legal_name_of_max_length_is_accepted(customer_api: CustomerApi) -> None:
    """La longitud máxima se aplica después del recorte."""

    legal_name = "X" * LEGAL_NAME_MAX_LENGTH
    payload = _valid_payload()
    payload["legal_name"] = f"  {legal_name}  "

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 201
    assert response.json()["legal_name"] == legal_name
    assert _stored_customers(customer_api)[0].legal_name == legal_name


def test_legal_name_over_max_length_returns_problem_422_and_does_not_persist(
    customer_api: CustomerApi,
) -> None:
    """Una razón social de 256 caracteres se rechaza antes de persistir."""

    payload = _valid_payload()
    payload["legal_name"] = "X" * (LEGAL_NAME_MAX_LENGTH + 1)

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_customers(customer_api) == []


def test_normalized_duplicate_tax_id_returns_problem_409(customer_api: CustomerApi) -> None:
    """La unicidad se comprueba después de normalizar el identificador fiscal."""

    first = asyncio.run(_post(customer_api.app, _valid_payload()))
    second_payload = _valid_payload()
    second_payload["tax_id"] = " B-12345674 "
    second = asyncio.run(_post(customer_api.app, second_payload))

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.headers["content-type"].startswith("application/problem+json")


def test_same_legal_name_with_different_tax_id_is_allowed(customer_api: CustomerApi) -> None:
    """La razón social no tiene restricción de unicidad."""

    first = asyncio.run(_post(customer_api.app, _valid_payload()))
    second_payload = _valid_payload()
    second_payload["tax_id"] = "12345678Z"
    second = asyncio.run(_post(customer_api.app, second_payload))

    assert first.status_code == 201
    assert second.status_code == 201
    assert len(_stored_customers(customer_api)) == 2


def test_duplicate_tax_id_returns_problem_409(customer_api: CustomerApi) -> None:
    """Un segundo alta con el mismo identificador fiscal devuelve 409."""

    first = asyncio.run(_post(customer_api.app, _valid_payload()))
    second = asyncio.run(_post(customer_api.app, _valid_payload()))

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.headers["content-type"].startswith("application/problem+json")
    body = second.json()
    assert body["status"] == 409
    assert VALID_TAX_ID in body["detail"]
    assert "sqlalchemy" not in second.text.lower()
    assert "traceback" not in second.text.lower()


@pytest.mark.parametrize("field", ["legal_name", "tax_id", "email", "country", "plan"])
def test_missing_required_field_returns_problem_422(
    customer_api: CustomerApi,
    field: str,
) -> None:
    """La ausencia de cualquiera de los cinco campos devuelve 422."""

    payload = _valid_payload()
    payload.pop(field)

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    errors = response.json()["errors"]
    assert any(error["field"] == f"body.{field}" for error in errors)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "no-es-un-email"),
        ("tax_id", "12345678A"),
        ("tax_id", "X1234567A"),
        ("tax_id", "B12345678"),
        ("country", "US"),
        ("plan", "premium"),
    ],
)
def test_invalid_value_returns_problem_422(
    customer_api: CustomerApi,
    field: str,
    value: str,
) -> None:
    """Email, identificador fiscal, país y plan inválidos devuelven 422."""

    payload = _valid_payload()
    payload[field] = value

    response = asyncio.run(_post(customer_api.app, payload))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    errors = response.json()["errors"]
    assert any(error["field"] in {field, f"body.{field}"} for error in errors)


def test_malformed_json_returns_problem_422(customer_api: CustomerApi) -> None:
    """Un cuerpo JSON mal formado se documenta como problema 422."""

    response = asyncio.run(_post(customer_api.app, raw_body="{no-es-json"))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["status"] == 422


def test_unexpected_error_returns_problem_500(customer_api: CustomerApi) -> None:
    """Un error no controlado devuelve 500 sin filtrar detalles internos."""

    def _broken_dependency() -> CreateCustomer:
        raise RuntimeError("detalle interno que no debe filtrarse")

    customer_api.app.dependency_overrides[get_create_customer_use_case] = _broken_dependency

    response = asyncio.run(
        _post(
            customer_api.app,
            _valid_payload(),
            raise_app_exceptions=False,
        )
    )

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    assert "detalle interno" not in response.text
    assert "traceback" not in response.text.lower()


def test_openapi_documents_customer_contract(customer_api: CustomerApi) -> None:
    """OpenAPI documenta ruta, esquemas y respuestas del alta."""

    response = asyncio.run(_get(customer_api.app, "/openapi.json"))

    assert response.status_code == 200
    payload = response.json()
    operation = payload["paths"]["/customers"]["post"]
    assert operation["responses"]["201"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/CustomerResponse"
    )
    for status_code in ("409", "422", "500"):
        assert "application/problem+json" in operation["responses"][status_code]["content"]

    schemas = payload["components"]["schemas"]
    assert "CustomerCreateRequest" in schemas
    assert "CustomerResponse" in schemas
    assert "ProblemDetails" in schemas
    assert "ProblemFieldError" in schemas
    assert "standard" in json.dumps(schemas)

    for schema_name in ("CustomerCreateRequest", "CustomerResponse"):
        legal_name_schema = schemas[schema_name]["properties"]["legal_name"]
        assert legal_name_schema["minLength"] == LEGAL_NAME_MIN_LENGTH
        assert legal_name_schema["maxLength"] == LEGAL_NAME_MAX_LENGTH


@pytest.mark.parametrize("country", ["ES", "PT", "FR", "DE", "IT", "NL"])
def test_supported_countries(customer_api: CustomerApi, country: str) -> None:
    """Los seis países conservan todos los campos y el único plan."""

    payload = {**_valid_payload(), "country": country}
    response = asyncio.run(_post(customer_api.app, payload))
    assert response.status_code == 201
    assert response.json()["country"] == country
    assert response.json()["plan"] == "standard"


def test_international_normalization_and_country_uniqueness(customer_api: CustomerApi) -> None:
    """Preserva puntuación y permite un mismo identificador en distintos países."""

    payload = {**_valid_payload(), "country": "FR", "tax_id": "  ab-12 /  34  "}
    first = asyncio.run(_post(customer_api.app, payload))
    assert first.status_code == 201
    assert first.json()["tax_id"] == "AB-12 / 34"
    duplicate = asyncio.run(_post(customer_api.app, {**payload, "tax_id": "AB-12 / 34"}))
    assert duplicate.status_code == 409
    assert duplicate.headers["content-type"].startswith("application/problem+json")
    other = asyncio.run(_post(customer_api.app, {**payload, "country": "DE"}))
    assert other.status_code == 201
    assert len(_stored_customers(customer_api)) == 2


@pytest.mark.parametrize("tax_id", ["", "   ", "X" * 65, "AB\n12", "AB\x0012", "AB\u200b12"])
def test_generic_tax_id_rejected(customer_api: CustomerApi, tax_id: str) -> None:
    """La validación genérica rechaza vacío, exceso y controles."""

    response = asyncio.run(
        _post(
            customer_api.app,
            {
                **_valid_payload(),
                "country": "PT",
                "tax_id": tax_id,
            },
        )
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert _stored_customers(customer_api) == []


def test_customers_continue_ignoring_extra_fields(customer_api: CustomerApi) -> None:
    """Q-26 no amplía unilateralmente el contrato de clientes."""

    response = asyncio.run(_post(customer_api.app, {**_valid_payload(), "unknown": 1}))
    assert response.status_code == 201
