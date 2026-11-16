"""Router HTTP de alta de clientes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status

from saas_o_matic.application.customers.dto import CreateCustomerCommand
from saas_o_matic.presentation.customers.dependencies import CreateCustomerUseCaseDep
from saas_o_matic.presentation.customers.schemas import (
    CustomerCreateRequest,
    CustomerResponse,
)

_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    status.HTTP_409_CONFLICT: {
        "description": "Ya existe un cliente con el identificador fiscal en el país.",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/ProblemDetails"}}
        },
    },
    status.HTTP_422_UNPROCESSABLE_CONTENT: {
        "description": "Datos de entrada no válidos.",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/ProblemDetails"}}
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Error interno no controlado.",
        "content": {
            "application/problem+json": {"schema": {"$ref": "#/components/schemas/ProblemDetails"}}
        },
    },
}

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dar de alta un cliente",
    description=(
        "Crea un cliente con los cinco campos obligatorios de FR-01. "
        "El plan debe pertenecer al catálogo aprobado del MVP."
    ),
    responses=_PROBLEM_RESPONSES,
)
def create_customer(
    payload: CustomerCreateRequest,
    use_case: CreateCustomerUseCaseDep,
) -> CustomerResponse:
    """Ejecuta el alta y devuelve la representación persistida."""

    result = use_case.execute(
        CreateCustomerCommand(
            legal_name=payload.legal_name,
            tax_id=payload.tax_id,
            email=str(payload.email),
            country=payload.country.value,
            plan=payload.plan.value,
        )
    )
    return CustomerResponse.model_validate(result, from_attributes=True)
