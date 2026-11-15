"""Construcción de la aplicación FastAPI de presentación."""

from fastapi import FastAPI

from saas_o_matic.presentation.health import router as health_router


def create_app() -> FastAPI:
    """Crea la aplicación HTTP sin lógica de negocio."""

    app = FastAPI(
        title="SaaS-O-Matic API",
        version="0.1.0",
        description="Scaffold inicial del backend de SaaS-O-Matic.",
    )
    app.include_router(health_router)
    return app
