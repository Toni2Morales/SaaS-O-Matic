"""Dependencias de presentación del módulo de simulaciones."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from saas_o_matic.application.simulations.queries import SimulationQueries
from saas_o_matic.application.simulations.use_cases import CreateSimulation, PreviewSimulation


def get_create_simulation_use_case() -> CreateSimulation:
    """Dependencia sustituida por el composition root con el adaptador real."""

    raise RuntimeError("El caso de uso de simulaciones no está configurado.")


CreateSimulationUseCaseDep = Annotated[
    CreateSimulation,
    Depends(get_create_simulation_use_case),
]


def get_preview_simulation_use_case() -> PreviewSimulation:
    raise RuntimeError("El caso de uso de preview no está configurado.")


def get_simulation_queries() -> SimulationQueries:
    raise RuntimeError("Las consultas de simulaciones no están configuradas.")


PreviewSimulationUseCaseDep = Annotated[PreviewSimulation, Depends(get_preview_simulation_use_case)]
SimulationQueriesDep = Annotated[SimulationQueries, Depends(get_simulation_queries)]
