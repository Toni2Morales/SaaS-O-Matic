"""Router HTTP de alta de clientes."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Query, status

from saas_o_matic.application.customers.dto import CreateCustomerCommand, ListCustomersQuery
from saas_o_matic.application.simulations.dto import SimulationHistoryQuery
from saas_o_matic.presentation.customers.dependencies import (
    CreateCustomerUseCaseDep,
    CustomerQueriesDep,
)
from saas_o_matic.presentation.customers.schemas import (
    CustomerCreateRequest,
    CustomerListParameters,
    CustomerPageResponse,
    CustomerResponse,
)
from saas_o_matic.presentation.pagination import PageParameters
from saas_o_matic.presentation.simulations.dependencies import SimulationQueriesDep
from saas_o_matic.presentation.simulations.schemas import (
    HistoricalSimulationResponse,
    SimulationHistoryPageResponse,
    simulation_values,
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


_READ_PROBLEMS: dict[int | str, dict[str, Any]] = {
    code: _PROBLEM_RESPONSES[code] for code in (422, 500)
}
_DETAIL_PROBLEMS: dict[int | str, dict[str, Any]] = {
    **_READ_PROBLEMS,
    404: {
        "description": "El cliente no existe.",
        "content": {
            "application/problem+json": {
                "schema": {"$ref": "#/components/schemas/ProblemDetails"},
            }
        },
    },
}


@router.get(
    "",
    response_model=CustomerPageResponse,
    responses=_READ_PROBLEMS,
    summary="Listar y buscar clientes",
    description=(
        "Búsqueda parcial Unicode casefold, sin quitar acentos; orden nombre casefold e id ASC."
    ),
)
def list_customers(
    parameters: Annotated[CustomerListParameters, Query()],
    queries: CustomerQueriesDep,
) -> CustomerPageResponse:
    result = queries.list(
        ListCustomersQuery(parameters.search, parameters.limit, parameters.offset)
    )
    return CustomerPageResponse.model_validate(result, from_attributes=True)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    responses=_DETAIL_PROBLEMS,
    summary="Consultar un cliente",
)
def get_customer(customer_id: UUID, queries: CustomerQueriesDep) -> CustomerResponse:
    return CustomerResponse.model_validate(queries.get(customer_id), from_attributes=True)


@router.get(
    "/{customer_id}/simulations",
    response_model=SimulationHistoryPageResponse,
    responses=_DETAIL_PROBLEMS,
    summary="Consultar historial inmutable",
    description="Orden created_at e id DESC; datos históricos desconocidos NULL, sin recalcular.",
)
def get_customer_simulations(
    customer_id: UUID,
    parameters: Annotated[PageParameters, Query()],
    queries: SimulationQueriesDep,
) -> SimulationHistoryPageResponse:
    result = queries.history(
        SimulationHistoryQuery(customer_id, parameters.limit, parameters.offset)
    )
    return SimulationHistoryPageResponse(
        items=[
            HistoricalSimulationResponse.model_validate(simulation_values(item))
            for item in result.items
        ],
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )
