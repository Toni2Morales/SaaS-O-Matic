"""Historial paginado: solo datos persistidos, sin estimador ni proveedor FX."""

from dataclasses import fields

from saas_o_matic.application.customers.errors import CustomerNotFound
from saas_o_matic.application.pagination import validate_pagination
from saas_o_matic.application.simulations.dto import (
    HistoricalSimulationResult,
    SimulationHistoryQuery,
    SimulationHistoryResult,
)
from saas_o_matic.domain.customers.ports import CustomerQueryRepository
from saas_o_matic.domain.simulations.calculation import MonthlyCalculation
from saas_o_matic.domain.simulations.entities import Simulation, format_eur_amount
from saas_o_matic.domain.simulations.ports import SimulationQueryRepository


def historical_result(simulation: Simulation) -> HistoricalSimulationResult:
    calculation: dict[str, str | None] = (
        simulation.calculation.snapshot()
        if simulation.calculation is not None
        else dict.fromkeys(field.name for field in fields(MonthlyCalculation))
    )
    return HistoricalSimulationResult(
        id=simulation.id,
        customer_id=simulation.customer_id,
        user_count=simulation.user_count,
        storage_gb=simulation.storage_gb,
        api_calls_per_month=simulation.api_calls_per_month,
        billing_period=simulation.billing_period,
        created_at=simulation.created_at,
        user_subtotal_eur=format_eur_amount(simulation.user_subtotal_eur),
        calculation=calculation,
    )


class SimulationQueries:
    def __init__(
        self,
        *,
        customers: CustomerQueryRepository,
        simulations: SimulationQueryRepository,
    ) -> None:
        self._customers = customers
        self._simulations = simulations

    def history(self, query: SimulationHistoryQuery) -> SimulationHistoryResult:
        validate_pagination(query.limit, query.offset)
        if not self._customers.exists_by_id(query.customer_id):
            raise CustomerNotFound("El cliente solicitado no existe.")
        simulations, total = self._simulations.list_for_customer(
            query.customer_id,
            limit=query.limit,
            offset=query.offset,
        )
        return SimulationHistoryResult(
            [historical_result(simulation) for simulation in simulations],
            total,
            query.limit,
            query.offset,
        )
