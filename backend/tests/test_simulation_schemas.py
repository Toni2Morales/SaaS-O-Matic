"""Pruebas de los esquemas Pydantic de simulaciones."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from saas_o_matic.presentation.simulations.schemas import (
    SimulationCreateRequest,
    SimulationResponse,
)


def _payload(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "customer_id": str(uuid4()),
        "user_count": 100,
    }
    values.update(overrides)
    return values


def test_request_accepts_the_approved_contract() -> None:
    """El esquema acepta UUID y entero estricto dentro del rango."""

    customer_id = uuid4()
    request = SimulationCreateRequest.model_validate(
        {"customer_id": str(customer_id), "user_count": 100}
    )

    assert request.customer_id == customer_id
    assert request.user_count == 100


@pytest.mark.parametrize("user_count", [1, 1_000_000])
def test_request_accepts_user_count_boundaries(user_count: int) -> None:
    """Los dos extremos del rango técnico son válidos."""

    request = SimulationCreateRequest.model_validate(_payload(user_count=user_count))

    assert request.user_count == user_count


@pytest.mark.parametrize(
    "user_count",
    [
        0,
        -1,
        1_000_001,
        10**100,
        10.0,
        10.5,
        "10",
        True,
        False,
        None,
    ],
)
def test_request_rejects_invalid_user_counts(user_count: object) -> None:
    """El esquema no coacciona tipos y aplica el rango técnico."""

    with pytest.raises(ValidationError):
        SimulationCreateRequest.model_validate(_payload(user_count=user_count))


@pytest.mark.parametrize("customer_id", ["no-es-un-uuid", "", None, 123])
def test_request_rejects_malformed_customer_id(customer_id: object) -> None:
    """El identificador de cliente debe ser un UUID válido."""

    with pytest.raises(ValidationError):
        SimulationCreateRequest.model_validate(_payload(customer_id=customer_id))


@pytest.mark.parametrize("field", ["customer_id", "user_count"])
def test_request_requires_all_fields(field: str) -> None:
    """Los dos campos del contrato son obligatorios."""

    payload = _payload()
    payload.pop(field)

    with pytest.raises(ValidationError):
        SimulationCreateRequest.model_validate(payload)


def test_request_ignores_unknown_fields_following_the_existing_policy() -> None:
    """Los campos no previstos se ignoran, como en el resto de esquemas actuales."""

    request = SimulationCreateRequest.model_validate(_payload(plan="standard", storage=10))

    assert request.user_count == 100
    assert "plan" not in request.model_dump()
    assert "storage" not in request.model_dump()


def test_request_schema_documents_user_count_bounds() -> None:
    """OpenAPI expone el rango del número de usuarios."""

    schema = SimulationCreateRequest.model_json_schema()
    user_count_schema = schema["properties"]["user_count"]

    assert user_count_schema["minimum"] == 1
    assert user_count_schema["maximum"] == 1_000_000


def test_response_serializes_decimal_string_and_utc_timestamp() -> None:
    """La respuesta conserva la cadena monetaria y usa sufijo ``Z``."""

    simulation_id = uuid4()
    customer_id = uuid4()
    response = SimulationResponse(
        id=simulation_id,
        customer_id=customer_id,
        user_count=100,
        user_subtotal_eur="670.00",
        created_at=datetime(2026, 11, 16, 16, 0, tzinfo=UTC),
    )

    payload = response.model_dump(mode="json")

    assert payload["id"] == str(simulation_id)
    assert payload["customer_id"] == str(customer_id)
    assert payload["user_count"] == 100
    assert payload["user_subtotal_eur"] == "670.00"
    assert payload["created_at"] == "2026-11-16T16:00:00Z"
    assert isinstance(payload["created_at"], str)
    assert isinstance(UUID(str(payload["id"])), UUID)
