"""Validación y cálculo compartidos por preview y guardado, sin persistencia."""

from dataclasses import dataclass
from decimal import Decimal

from saas_o_matic.application.simulations.dto import (
    MAX_API_CALLS_PER_MONTH,
    MAX_SIMULATION_USER_COUNT,
    MAX_STORAGE_GB,
    CreateSimulationCommand,
)
from saas_o_matic.application.simulations.errors import (
    ConversionUnavailable,
    InvalidSimulationData,
    SimulationCustomerNotFound,
)
from saas_o_matic.application.simulations.estimator import MonthlyEstimator
from saas_o_matic.domain.customers.ports import CustomerRepository
from saas_o_matic.domain.pricing.errors import InvalidUserCount
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
from saas_o_matic.domain.simulations.calculation import (
    Currency,
    MonthlyCalculation,
    RateUnavailable,
)


@dataclass(frozen=True, slots=True)
class PreparedSimulation:
    subtotal: Decimal
    calculation: MonthlyCalculation


class CalculateSimulation:
    def __init__(self, *, customers: CustomerRepository, estimator: MonthlyEstimator) -> None:
        self._customers = customers
        self._estimator = estimator

    def execute(self, command: CreateSimulationCommand) -> PreparedSimulation:
        self._validate_user_count(command.user_count)
        for field, value, maximum in (
            ("storage_gb", command.storage_gb, MAX_STORAGE_GB),
            ("api_calls_per_month", command.api_calls_per_month, MAX_API_CALLS_PER_MONTH),
        ):
            if type(value) is not int or not 0 <= value <= maximum:
                raise InvalidSimulationData(field, f"Debe ser un entero entre 0 y {maximum}.")
        try:
            currency = Currency(command.display_currency)
        except ValueError as exc:
            raise InvalidSimulationData("display_currency", "Divisa no soportada.") from exc
        country = self._customers.get_country_by_id(command.customer_id)
        if country is None:
            raise SimulationCustomerNotFound(command.customer_id)
        try:
            subtotal = calculate_user_subtotal(command.user_count)
        except InvalidUserCount as exc:
            raise InvalidSimulationData("user_count", str(exc)) from exc
        try:
            calculation = self._estimator.estimate(subtotal, country, currency)
        except RateUnavailable as exc:
            raise ConversionUnavailable("Proveedor de divisas no disponible.") from exc
        return PreparedSimulation(subtotal, calculation)

    @staticmethod
    def _validate_user_count(user_count: object) -> None:
        if isinstance(user_count, bool) or not isinstance(user_count, int):
            raise InvalidSimulationData("user_count", "El número de usuarios debe ser un entero.")
        if user_count < 0:
            raise InvalidSimulationData(
                "user_count", "El número de usuarios debe ser un entero no negativo."
            )
        if user_count > MAX_SIMULATION_USER_COUNT:
            raise InvalidSimulationData(
                "user_count",
                f"El número de usuarios no puede superar {MAX_SIMULATION_USER_COUNT}.",
            )
