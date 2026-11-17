"""Puertos del dominio de simulaciones."""

from __future__ import annotations

from typing import Protocol

from saas_o_matic.domain.simulations.entities import Simulation


class SimulationRepository(Protocol):
    """Puerto de persistencia para simulaciones."""

    def add(self, simulation: Simulation) -> None:
        """Persiste la simulación y confirma la transacción."""
