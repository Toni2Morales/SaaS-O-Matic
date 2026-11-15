"""Pruebas mínimas de infraestructura HTTP."""

import asyncio

from httpx import ASGITransport, AsyncClient, Response

from saas_o_matic.bootstrap.main import app


async def _get(path: str) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.get(path)


def test_health_returns_ok() -> None:
    """El endpoint de salud responde con el contrato mínimo esperado."""

    response = asyncio.run(_get("/health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema_is_available() -> None:
    """FastAPI publica el esquema OpenAPI generado."""

    response = asyncio.run(_get("/openapi.json"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["openapi"].startswith("3.")
    assert "/health" in payload["paths"]
