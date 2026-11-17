"""Caso de uso de creación de simulaciones."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from saas_o_matic.application.simulations.dto import (
    MAX_SIMULATION_USER_COUNT,
    CreateSimulationCommand,
    SimulationResult,
)
from saas_o_matic.application.simulations.errors import (
    InvalidSimulationData,
    SimulationCustomerNotFound,
)
from saas_o_matic.domain.customers.ports import CustomerRepository
from saas_o_matic.domain.pricing.errors import InvalidUserCount
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
from saas_o_matic.domain.simulations.entities import Simulation, format_eur_amount
from saas_o_matic.domain.simulations.ports import SimulationRepository


class CreateSimulation:
    """Caso de uso de creación de una simulación persistida.

    El subtotal se calcula con el motor de precios existente. El máximo técnico
    de la API se valida en aplicación y no se incorpora al dominio de precios.
    """

    def __init__(
        self,
        *,
        simulations: SimulationRepository,
        customers: CustomerRepository,
    ) -> None:
        self._simulations = simulations
        self._customers = customers

    def execute(self, command: CreateSimulationCommand) -> SimulationResult:
        """Valida, calcula, comprueba el cliente y persiste la simulación."""

        self._validate_user_count(command.user_count)

        try:
            subtotal = calculate_user_subtotal(command.user_count)
        except InvalidUserCount as exc:
            raise InvalidSimulationData("user_count", str(exc)) from exc

        if not self._customers.exists_by_id(command.customer_id):
            raise SimulationCustomerNotFound(command.customer_id)

        simulation = Simulation(
            id=uuid4(),
            customer_id=command.customer_id,
            user_count=command.user_count,
            user_subtotal_eur=subtotal,
            created_at=datetime.now(UTC),
        )
        self._simulations.add(simulation)

        return SimulationResult(
            id=simulation.id,
            customer_id=simulation.customer_id,
            user_count=simulation.user_count,
            user_subtotal_eur=format_eur_amount(simulation.user_subtotal_eur),
            created_at=simulation.created_at,
        )

    @staticmethod
    def _validate_user_count(user_count: object) -> None:
        """Aplica el rango técnico admitido por este incremento."""

        if isinstance(user_count, bool) or not isinstance(user_count, int):
            raise InvalidSimulationData(
                "user_count",
                "El número de usuarios debe ser un entero.",
            )
        if user_count < 1:
            raise InvalidSimulationData(
                "user_count",
                "El número de usuarios debe ser un entero positivo.",
            )
        if user_count > MAX_SIMULATION_USER_COUNT:
            raise InvalidSimulationData(
                "user_count",
                f"El número de usuarios no puede superar {MAX_SIMULATION_USER_COUNT}.",
            )
