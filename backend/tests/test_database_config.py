"""Resolución única de SQLite para runtime y Alembic, sin tocar la base real."""

from __future__ import annotations

import asyncio
import hashlib
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import text

from saas_o_matic.bootstrap import main
from saas_o_matic.infrastructure.database import (
    DEFAULT_DATABASE_PATH,
    DEFAULT_DATABASE_URL,
    create_sqlite_engine,
    database_path_from_url,
    resolve_database_path,
    resolve_database_url,
)

ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"
EXPECTED_REVISION = "0004_add_simulation_taxes_and_fx"


def _alembic_config(database_url: str) -> Config:
    config = Config(str(ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _database_url(path: Path) -> str:
    return f"sqlite:///{path.as_posix()}"


def _snapshot(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def _request(
    method: str,
    path: str,
    payload: dict[str, object] | None = None,
) -> Response:
    transport = ASGITransport(app=main.app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, json=payload)


def test_default_resolution_preserves_backend_var_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    assert resolve_database_url() == DEFAULT_DATABASE_URL
    assert resolve_database_path() == DEFAULT_DATABASE_PATH.resolve()


def test_environment_url_wins_over_configured_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    environment_path = tmp_path / "environment.sqlite3"
    monkeypatch.setenv("DATABASE_URL", _database_url(environment_path))

    assert resolve_database_url("sqlite:///./other.sqlite3") == _database_url(
        environment_path.resolve()
    )
    assert resolve_database_path() == environment_path.resolve()


def test_configured_url_is_used_when_environment_is_absent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    configured_path = tmp_path / "configured.sqlite3"

    assert database_path_from_url(resolve_database_url(_database_url(configured_path))) == (
        configured_path.resolve()
    )


def test_relative_url_is_anchored_to_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    resolved = resolve_database_path("sqlite:///./var/relative.sqlite3")

    assert resolved == (DEFAULT_DATABASE_PATH.parent / "relative.sqlite3").resolve()


@pytest.mark.parametrize(
    "url",
    [
        "postgresql://user@localhost/database",
        "sqlite:///:memory:",
        "sqlite://",
        "sqlite:///file.sqlite3?mode=ro",
        "not a url",
    ],
)
def test_invalid_database_configuration_is_rejected(
    url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", url)

    with pytest.raises(ValueError):
        resolve_database_url()


def test_blank_environment_url_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "   ")

    assert resolve_database_url() == DEFAULT_DATABASE_URL


def test_runtime_rejects_invalid_configuration_without_opening_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://user@localhost/database")
    monkeypatch.setattr(main, "_session_factory", None)

    with pytest.raises(ValueError, match="SQLite"):
        main._get_session_factory()


def test_alembic_and_runtime_share_alternative_database(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    alternative_path = tmp_path / "alternative.sqlite3"
    unrelated_path = tmp_path / "unrelated.sqlite3"
    monkeypatch.setenv("DATABASE_URL", _database_url(alternative_path))
    monkeypatch.setattr(main, "_session_factory", None)
    default_before = _snapshot(DEFAULT_DATABASE_PATH)

    command.upgrade(_alembic_config(_database_url(unrelated_path)), "head")

    assert alternative_path.exists()
    assert not unrelated_path.exists()
    created = asyncio.run(
        _request(
            "POST",
            "/customers",
            {
                "legal_name": "Cliente de configuración temporal",
                "tax_id": "B12345674",
                "email": "config@example.com",
                "country": "ES",
                "plan": "standard",
            },
        )
    )
    assert created.status_code == 201
    customer_id = created.json()["id"]

    retrieved = asyncio.run(_request("GET", f"/customers/{customer_id}"))
    assert retrieved.status_code == 200
    assert retrieved.json()["id"] == customer_id

    engine = create_sqlite_engine(alternative_path)
    try:
        with engine.connect() as connection:
            assert connection.execute(text("SELECT COUNT(*) FROM customers")).scalar_one() == 1
            assert (
                connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
                == EXPECTED_REVISION
            )
    finally:
        engine.dispose()

    assert _snapshot(DEFAULT_DATABASE_PATH) == default_before
