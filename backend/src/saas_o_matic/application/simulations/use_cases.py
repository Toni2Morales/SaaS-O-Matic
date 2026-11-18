"""Caso de uso de creación de simulaciones."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from saas_o_matic.application.simulations.calculator import CalculateSimulation, PreparedSimulation
from saas_o_matic.application.simulations.dto import (
    CreateSimulationCommand,
    PreviewSimulationResult,
    SimulationResult,
)
from saas_o_matic.application.simulations.estimator import MonthlyEstimator
from saas_o_matic.domain.customers.ports import CustomerRepository
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
        estimator: MonthlyEstimator,
    ) -> None:
        self._simulations = simulations
        self._calculator = CalculateSimulation(customers=customers, estimator=estimator)

    def execute(self, command: CreateSimulationCommand) -> SimulationResult:
        """Valida, comprueba el cliente, calcula y persiste la simulación."""

        prepared = self._calculator.execute(command)

        simulation = Simulation(
            id=uuid4(),
            customer_id=command.customer_id,
            user_count=command.user_count,
            user_subtotal_eur=prepared.subtotal,
            created_at=datetime.now(UTC),
            storage_gb=command.storage_gb,
            api_calls_per_month=command.api_calls_per_month,
            calculation=prepared.calculation,
        )
        self._simulations.add(simulation)

        return SimulationResult(
            id=simulation.id,
            customer_id=simulation.customer_id,
            user_count=simulation.user_count,
            user_subtotal_eur=format_eur_amount(simulation.user_subtotal_eur),
            created_at=simulation.created_at,
            storage_gb=command.storage_gb,
            api_calls_per_month=command.api_calls_per_month,
            billing_period=simulation.billing_period,
            calculation=prepared.calculation.snapshot(),
        )


def _preview_result(
    command: CreateSimulationCommand,
    prepared: PreparedSimulation,
) -> PreviewSimulationResult:
    return PreviewSimulationResult(
        customer_id=command.customer_id,
        user_count=command.user_count,
        storage_gb=command.storage_gb,
        api_calls_per_month=command.api_calls_per_month,
        billing_period="monthly",
        user_subtotal_eur=format_eur_amount(prepared.subtotal),
        calculation=prepared.calculation.snapshot(),
    )


class PreviewSimulation:
    """Solo lectura/cálculo; no recibe ningún repositorio de simulaciones."""

    def __init__(self, *, customers: CustomerRepository, estimator: MonthlyEstimator) -> None:
        self._calculator = CalculateSimulation(customers=customers, estimator=estimator)

    def execute(self, command: CreateSimulationCommand) -> PreviewSimulationResult:
        return _preview_result(command, self._calculator.execute(command))
