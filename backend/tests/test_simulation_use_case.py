"""Pruebas del caso de uso de creación de simulaciones."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC
from decimal import Decimal, Inexact, Rounded, localcontext
from typing import Any, cast
from uuid import UUID, uuid4

import pytest

from saas_o_matic.application.simulations.dto import CreateSimulationCommand
from saas_o_matic.application.simulations.errors import (
    InvalidSimulationData,
    SimulationCustomerNotFound,
)
from saas_o_matic.application.simulations.use_cases import CreateSimulation
from saas_o_matic.bootstrap.simulations import shared_estimator
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.ports import CustomerRepository
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    TaxId,
)
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
from saas_o_matic.domain.simulations.entities import (
    InvalidSimulationAmount,
    Simulation,
    format_eur_amount,
)


class InMemoryCustomerRepository:
    """Doble de prueba que solo necesita comprobar existencia por id."""

    def __init__(self, customer_ids: set[UUID] | None = None) -> None:
        self.customer_ids = customer_ids or set()
        self.customers: list[Customer] = []

    def exists_by_tax_id(self, tax_id: TaxId, country: CountryCode) -> bool:
        return False

    def exists_by_id(self, customer_id: UUID) -> bool:
        return customer_id in self.customer_ids

    def get_country_by_id(self, customer_id: UUID) -> CountryCode | None:
        return CountryCode.ES if customer_id in self.customer_ids else None

    def add(self, customer: Customer) -> None:
        self.customers.append(customer)


class InMemorySimulationRepository:
    """Doble de prueba que conserva las simulaciones persistidas."""

    def __init__(self) -> None:
        self.simulations: list[Simulation] = []

    def add(self, simulation: Simulation) -> None:
        self.simulations.append(simulation)


def _command(
    *, customer_id: UUID | None = None, user_count: object = 100
) -> CreateSimulationCommand:
    return CreateSimulationCommand(
        customer_id=customer_id or uuid4(),
        user_count=cast(int, user_count),
        storage_gb=250,
        api_calls_per_month=100000,
    )


def _use_case(
    customer_ids: set[UUID],
) -> tuple[CreateSimulation, InMemorySimulationRepository]:
    customers: CustomerRepository = InMemoryCustomerRepository(customer_ids)
    simulations = InMemorySimulationRepository()
    return (
        CreateSimulation(
            simulations=simulations, customers=customers, estimator=shared_estimator()
        ),
        simulations,
    )


@pytest.mark.parametrize(
    ("user_count", "expected"),
    [
        (0, "0.00"),
        (15, "140.00"),
        (1, "10.00"),
        (10, "100.00"),
        (11, "108.00"),
        (50, "420.00"),
        (51, "425.00"),
        (100, "670.00"),
        (1_000_000, "5000170.00"),
    ],
)
def test_create_simulation_returns_the_approved_subtotals(
    user_count: int,
    expected: str,
) -> None:
    """El caso de uso reutiliza pricing y devuelve la cadena exacta."""

    customer_id = uuid4()
    use_case, simulations = _use_case({customer_id})

    result = use_case.execute(_command(customer_id=customer_id, user_count=user_count))

    assert isinstance(result.id, UUID)
    assert result.customer_id == customer_id
    assert result.user_count == user_count
    assert result.user_subtotal_eur == expected
    assert result.created_at.tzinfo is UTC
    assert len(simulations.simulations) == 1
    assert simulations.simulations[0].user_subtotal_eur == Decimal(expected)


def test_create_simulation_reuses_the_pricing_engine() -> None:
    """El resultado coincide con el cálculo del motor existente."""

    customer_id = uuid4()
    use_case, _ = _use_case({customer_id})

    result = use_case.execute(_command(customer_id=customer_id, user_count=123))

    assert result.user_subtotal_eur == format_eur_amount(calculate_user_subtotal(123))


def test_create_simulation_rejects_unknown_customer_without_persisting() -> None:
    """Un UUID válido no registrado produce un error de aplicación."""

    use_case, simulations = _use_case(set())

    with pytest.raises(SimulationCustomerNotFound):
        use_case.execute(_command())

    assert simulations.simulations == []


@pytest.mark.parametrize(
    "user_count",
    [-1, 1_000_001, 10**100, 10.0, "10", True, False, None, Decimal("10")],
)
def test_create_simulation_rejects_invalid_user_count_without_persisting(
    user_count: object,
) -> None:
    """La validación defensiva aplica el rango técnico antes de calcular."""

    customer_id = uuid4()
    use_case, simulations = _use_case({customer_id})

    with pytest.raises(InvalidSimulationData) as error:
        use_case.execute(_command(customer_id=customer_id, user_count=user_count))

    assert error.value.field == "user_count"
    assert simulations.simulations == []


def test_format_eur_amount_is_exact_and_does_not_round() -> None:
    """La representación canónica no redondea cantidades con más precisión."""

    assert format_eur_amount(Decimal("10")) == "10.00"
    assert format_eur_amount(Decimal("10.0")) == "10.00"
    assert format_eur_amount(Decimal("5000170.00")) == "5000170.00"

    with pytest.raises(InvalidSimulationAmount):
        format_eur_amount(Decimal("10.005"))


def test_simulation_entity_rejects_invalid_basic_invariants() -> None:
    """La entidad no acepta usuarios negativos."""

    with pytest.raises(ValueError):
        Simulation(
            id=uuid4(),
            customer_id=uuid4(),
            user_count=-1,
            user_subtotal_eur=Decimal("0.00"),
            created_at=cast(Any, None),
        )


def test_money_formatter_isolates_traps_and_flags() -> None:
    """Traps heredados no filtran excepciones decimales ni alteran el contexto."""

    with localcontext() as context:
        context.prec = 2
        context.traps[Inexact] = True
        context.traps[Rounded] = True
        before = (context.prec, dict(context.traps), dict(context.flags))
        assert format_eur_amount(Decimal("140.000")) == "140.00"
        assert format_eur_amount(Decimal("-0.000")) == "0.00"
        with pytest.raises(InvalidSimulationAmount):
            format_eur_amount(Decimal("1.001"))
        assert (context.prec, dict(context.traps), dict(context.flags)) == before


@pytest.mark.parametrize("amount", ["NaN", "sNaN", "Infinity", "-1", "0.001"])
def test_formatter_invalid_values_raise_domain_errors_with_all_traps(amount: str) -> None:
    with localcontext() as context:
        for signal in context.traps:
            context.traps[signal] = True
        before = dict(context.flags)
        with pytest.raises(InvalidSimulationAmount):
            format_eur_amount(Decimal(amount))
        assert dict(context.flags) == before


def test_customer_checked_before_pricing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un cliente inexistente no dispara el motor comercial."""

    def forbidden(count: int) -> Decimal:
        pytest.fail("No debe calcularse antes de comprobar el cliente")

    monkeypatch.setattr(
        "saas_o_matic.application.simulations.calculator.calculate_user_subtotal",
        forbidden,
    )
    use_case, simulations = _use_case(set())
    with pytest.raises(SimulationCustomerNotFound):
        use_case.execute(_command())
    assert simulations.simulations == []


@pytest.mark.parametrize("field", ["storage_gb", "api_calls_per_month"])
@pytest.mark.parametrize("value", [-1, True, False, 1.0, "1", None, 1000000001])
def test_application_rejects_invalid_consumption(field: str, value: object) -> None:
    customer_id = uuid4()
    use_case, simulations = _use_case({customer_id})
    command = replace(_command(customer_id=customer_id), **{field: cast(Any, value)})
    with pytest.raises(InvalidSimulationData) as error:
        use_case.execute(command)
    assert error.value.field == field
    assert simulations.simulations == []


def test_entity_rejects_non_decimal_amount() -> None:
    with pytest.raises(InvalidSimulationAmount):
        Simulation(
            id=uuid4(),
            customer_id=uuid4(),
            user_count=1,
            user_subtotal_eur=cast(Any, "10.00"),
            created_at=cast(Any, None),
        )
