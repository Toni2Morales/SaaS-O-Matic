"""Router HTTP de creación de simulaciones."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status

from saas_o_matic.application.simulations.dto import CreateSimulationCommand
from saas_o_matic.presentation.simulations.dependencies import CreateSimulationUseCaseDep
from saas_o_matic.presentation.simulations.schemas import (
    SimulationCreateRequest,
    SimulationResponse,
)

_PROBLEM_RESPONSES: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
        "description": "El cliente indicado no existe.",
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

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post(
    "",
    response_model=SimulationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una simulación",
    description=(
        "Crea una simulación de coste de usuarios para un cliente registrado. "
        "El primer incremento calcula únicamente el subtotal de usuarios en EUR."
    ),
    responses=_PROBLEM_RESPONSES,
)
def create_simulation(
    payload: SimulationCreateRequest,
    use_case: CreateSimulationUseCaseDep,
) -> SimulationResponse:
    """Ejecuta el caso de uso y devuelve la simulación persistida."""

    result = use_case.execute(
        CreateSimulationCommand(
            customer_id=payload.customer_id,
            user_count=payload.user_count,
        )
    )
    return SimulationResponse.model_validate(result, from_attributes=True)
