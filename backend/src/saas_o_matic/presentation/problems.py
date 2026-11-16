"""Respuestas de error controladas con ``application/problem+json``."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from saas_o_matic.application.customers.errors import (
    CustomerTaxIdAlreadyExists,
    InvalidCustomerData,
)


class ProblemFieldError(BaseModel):
    """Error asociado a un campo concreto de la petición."""

    field: str
    message: str


class ProblemDetails(BaseModel):
    """Esquema de error basado en RFC 9457."""

    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
    errors: list[ProblemFieldError] | None = None


def problem_response(
    *,
    status: int,
    title: str,
    detail: str,
    instance: str | None = None,
    errors: list[ProblemFieldError] | None = None,
) -> JSONResponse:
    """Construye una respuesta ``application/problem+json``."""

    problem = ProblemDetails(
        type="about:blank",
        title=title,
        status=status,
        detail=detail,
        instance=instance,
        errors=errors,
    )
    return JSONResponse(
        status_code=status,
        content=problem.model_dump(exclude_none=True),
        media_type="application/problem+json",
    )


def register_problem_handlers(app: FastAPI) -> None:
    """Registra los manejadores de errores controlados de clientes."""

    app.add_exception_handler(RequestValidationError, _handle_request_validation_error)
    app.add_exception_handler(InvalidCustomerData, _handle_invalid_customer_data)
    app.add_exception_handler(CustomerTaxIdAlreadyExists, _handle_tax_id_conflict)
    app.add_exception_handler(Exception, _handle_unexpected_error)


def add_problem_schema_to_openapi(app: FastAPI) -> None:
    """Añade el esquema de problema a los componentes OpenAPI."""

    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema is not None:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        problem_schema = ProblemDetails.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
        definitions = problem_schema.pop("$defs", {})
        components.update(definitions)
        components["ProblemDetails"] = problem_schema
        app.openapi_schema = schema
        return schema

    # FastAPI permite sustituir el generador de OpenAPI en la instancia.
    app.openapi = custom_openapi  # type: ignore[method-assign]


async def _handle_request_validation_error(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        return _handle_unexpected_error_response(request)

    errors = [
        ProblemFieldError(
            field=".".join(str(part) for part in error["loc"]),
            message=error["msg"],
        )
        for error in exc.errors()
    ]
    return problem_response(
        status=422,
        title="Datos de cliente no válidos",
        detail="La petición no cumple el esquema esperado.",
        instance=request.url.path,
        errors=errors,
    )


async def _handle_invalid_customer_data(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, InvalidCustomerData):
        return _handle_unexpected_error_response(request)

    return problem_response(
        status=422,
        title="Datos de cliente no válidos",
        detail=exc.message,
        instance=request.url.path,
        errors=[ProblemFieldError(field=exc.field, message=exc.message)],
    )


async def _handle_tax_id_conflict(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, CustomerTaxIdAlreadyExists):
        return _handle_unexpected_error_response(request)

    return problem_response(
        status=409,
        title="Conflicto de identificador fiscal",
        detail=str(exc),
        instance=request.url.path,
    )


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    return _handle_unexpected_error_response(request)


def _handle_unexpected_error_response(request: Request) -> JSONResponse:
    return problem_response(
        status=500,
        title="Error interno del servidor",
        detail="Se ha producido un error interno.",
        instance=request.url.path,
    )
