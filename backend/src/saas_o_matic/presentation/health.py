"""Endpoint de infraestructura para comprobar que la aplicación responde."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Respuesta mínima del endpoint de salud."""

    status: str


router = APIRouter(tags=["infrastructure"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Devuelve el estado básico de la aplicación."""

    return HealthResponse(status="ok")
