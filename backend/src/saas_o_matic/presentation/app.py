"""Construcción de la aplicación FastAPI de presentación."""

from fastapi import FastAPI

from saas_o_matic.presentation.customers.router import router as customers_router
from saas_o_matic.presentation.health import router as health_router
from saas_o_matic.presentation.problems import (
    add_problem_schema_to_openapi,
    register_problem_handlers,
)
from saas_o_matic.presentation.simulations.router import router as simulations_router


def create_app() -> FastAPI:
    """Crea la aplicación HTTP con las rutas aprobadas."""

    app = FastAPI(
        title="SaaS-O-Matic API",
        version="0.1.0",
        description="Backend de SaaS-O-Matic.",
    )
    register_problem_handlers(app)
    add_problem_schema_to_openapi(app)
    app.include_router(health_router)
    app.include_router(customers_router)
    app.include_router(simulations_router)
    return app
