"""Pruebas de los esquemas Pydantic de clientes."""

import pytest
from pydantic import ValidationError

from saas_o_matic.application.customers.catalogs import (
    LEGAL_NAME_MAX_LENGTH,
    LEGAL_NAME_MIN_LENGTH,
    CountryCode,
    PlanCode,
)
from saas_o_matic.presentation.customers.schemas import (
    CustomerCreateRequest,
    CustomerResponse,
)

STANDARD_PLAN = PlanCode.STANDARD


def test_customer_create_request_requires_all_fr_01_fields() -> None:
    """El contrato exige los cinco campos de FR-01."""

    request = CustomerCreateRequest(
        legal_name="Cliente de prueba",
        tax_id="12345678Z",
        email="cliente@example.com",
        country="ES",
        plan="standard",
    )

    assert request.email == "cliente@example.com"
    assert request.country is CountryCode.ES
    assert request.plan is PlanCode.STANDARD
    assert request.plan.value == "standard"
    assert "id" not in CustomerCreateRequest.model_fields


def test_customer_create_request_normalizes_legal_name() -> None:
    """Pydantic recorta la razón social y conserva los espacios interiores."""

    request = CustomerCreateRequest(
        legal_name="  Empresa  Ejemplo S.L.  ",
        tax_id="12345678Z",
        email="cliente@example.com",
        country="ES",
        plan="standard",
    )

    assert request.legal_name == "Empresa  Ejemplo S.L."


@pytest.mark.parametrize("legal_name", ["", "   ", "\t\n"])
def test_customer_create_request_rejects_blank_legal_name(legal_name: str) -> None:
    """Una razón social vacía o compuesta solo por espacios no es válida."""

    with pytest.raises(ValidationError):
        CustomerCreateRequest(
            legal_name=legal_name,
            tax_id="12345678Z",
            email="cliente@example.com",
            country="ES",
            plan="standard",
        )


def test_customer_create_request_accepts_legal_name_length_boundaries() -> None:
    """La longitud se valida después del recorte, entre 1 y 255 caracteres."""

    one_character = CustomerCreateRequest(
        legal_name="A",
        tax_id="12345678Z",
        email="cliente@example.com",
        country="ES",
        plan="standard",
    )
    max_length = CustomerCreateRequest(
        legal_name=f"  {'X' * LEGAL_NAME_MAX_LENGTH}  ",
        tax_id="12345678Z",
        email="cliente@example.com",
        country="ES",
        plan="standard",
    )

    assert one_character.legal_name == "A"
    assert max_length.legal_name == "X" * LEGAL_NAME_MAX_LENGTH

    with pytest.raises(ValidationError):
        CustomerCreateRequest(
            legal_name="X" * (LEGAL_NAME_MAX_LENGTH + 1),
            tax_id="12345678Z",
            email="cliente@example.com",
            country="ES",
            plan="standard",
        )


def test_customer_create_request_schema_documents_legal_name_bounds() -> None:
    """OpenAPI expone los límites de longitud de ``legal_name``."""

    schema = CustomerCreateRequest.model_json_schema()
    legal_name_schema = schema["properties"]["legal_name"]

    assert legal_name_schema["minLength"] == LEGAL_NAME_MIN_LENGTH
    assert legal_name_schema["maxLength"] == LEGAL_NAME_MAX_LENGTH


@pytest.mark.parametrize("email", ["no-es-un-email", "usuario@", "@example.com"])
def test_customer_create_request_rejects_invalid_email(email: str) -> None:
    """El email se valida sintácticamente con ``EmailStr``."""

    with pytest.raises(ValidationError):
        CustomerCreateRequest(
            legal_name="Cliente de prueba",
            tax_id="12345678Z",
            email=email,
            country="ES",
            plan=STANDARD_PLAN,
        )


def test_customer_create_request_rejects_unsupported_country() -> None:
    """La primera versión solo admite el código ISO ``ES``."""

    with pytest.raises(ValidationError):
        CustomerCreateRequest(
            legal_name="Cliente de prueba",
            tax_id="12345678Z",
            email="cliente@example.com",
            country="FR",
            plan=STANDARD_PLAN,
        )


def test_customer_create_request_requires_plan() -> None:
    """No se crea un contrato de cuatro campos sin ``plan``."""

    with pytest.raises(ValidationError):
        CustomerCreateRequest.model_validate(
            {
                "legal_name": "Cliente de prueba",
                "tax_id": "12345678Z",
                "email": "cliente@example.com",
                "country": "ES",
            }
        )


@pytest.mark.parametrize("plan", ["premium", "", "STANDARD"])
def test_customer_create_request_rejects_unsupported_plan(plan: str) -> None:
    """El plan debe pertenecer exactamente al catálogo aprobado."""

    with pytest.raises(ValidationError):
        CustomerCreateRequest(
            legal_name="Cliente de prueba",
            tax_id="12345678Z",
            email="cliente@example.com",
            country="ES",
            plan=plan,
        )


def test_customer_response_contains_the_created_representation() -> None:
    """La respuesta devuelve los campos del cliente creado."""

    response = CustomerResponse(
        id="00000000-0000-0000-0000-000000000001",
        legal_name="Cliente de prueba",
        tax_id="12345678Z",
        email="cliente@example.com",
        country="ES",
        plan=STANDARD_PLAN,
        created_at="2026-11-15T12:00:00Z",
    )

    assert response.country is CountryCode.ES
    assert response.plan is PlanCode.STANDARD
