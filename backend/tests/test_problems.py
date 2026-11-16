"""Pruebas de las respuestas ``application/problem+json``."""

from __future__ import annotations

import asyncio

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response

from saas_o_matic.application.customers.errors import (
    CustomerTaxIdAlreadyExists,
    InvalidCustomerData,
)
from saas_o_matic.presentation.customers.schemas import CustomerCreateRequest
from saas_o_matic.presentation.problems import ProblemDetails, register_problem_handlers


async def _get(
    app: FastAPI,
    path: str,
    *,
    raise_app_exceptions: bool = True,
) -> Response:
    transport = ASGITransport(app=app, raise_app_exceptions=raise_app_exceptions)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.get(path)


async def _post(app: FastAPI, path: str, payload: dict[str, str]) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.post(path, json=payload)


def _problem_app() -> FastAPI:
    app = FastAPI()
    register_problem_handlers(app)

    @app.get("/invalid")
    def invalid() -> None:
        raise InvalidCustomerData("tax_id", "Identificador fiscal no válido.")

    @app.get("/conflict")
    def conflict() -> None:
        raise CustomerTaxIdAlreadyExists("12345678Z", "ES")

    @app.get("/unexpected")
    def unexpected() -> None:
        raise RuntimeError("detalle interno que no debe filtrarse")

    @app.post("/validate")
    def validate(payload: CustomerCreateRequest) -> dict[str, str]:
        return {"status": "ok"}

    return app


def test_validation_error_uses_problem_json() -> None:
    """Un error de validación se devuelve con el esquema de problema."""

    response = asyncio.run(_get(_problem_app(), "/invalid"))

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["status"] == 422
    assert payload["title"] == "Datos de cliente no válidos"
    assert payload["instance"] == "/invalid"
    assert payload["errors"] == [{"field": "tax_id", "message": "Identificador fiscal no válido."}]


def test_request_validation_error_uses_problem_json() -> None:
    """Los errores de esquema de FastAPI también usan el formato de problema."""

    response = asyncio.run(
        _post(
            _problem_app(),
            "/validate",
            {
                "legal_name": "Cliente de prueba",
                "tax_id": "12345678Z",
                "email": "cliente@example.com",
                "country": "ES",
            },
        )
    )

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["status"] == 422
    assert any(error["field"] == "body.plan" for error in payload["errors"])


def test_conflict_uses_problem_json() -> None:
    """Un conflicto de unicidad se devuelve con el esquema de problema."""

    response = asyncio.run(_get(_problem_app(), "/conflict"))

    assert response.status_code == 409
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["status"] == 409
    assert payload["title"] == "Conflicto de identificador fiscal"
    assert "12345678Z" in payload["detail"]


def test_unexpected_error_does_not_leak_internal_details() -> None:
    """Un error interno se devuelve sin el mensaje de la excepción original."""

    response = asyncio.run(_get(_problem_app(), "/unexpected", raise_app_exceptions=False))

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["status"] == 500
    assert "detalle interno" not in payload["detail"]


def test_problem_details_schema_is_documented() -> None:
    """El esquema de problema expone los campos que se documentarán en OpenAPI."""

    schema = ProblemDetails.model_json_schema()

    assert {"type", "title", "status", "detail", "instance", "errors"} <= set(schema["properties"])
