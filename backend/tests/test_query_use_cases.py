"""Validaciones defensivas de aplicación sin SQL ni frameworks."""

from typing import Any, cast
from uuid import UUID

import pytest

from saas_o_matic.application.customers.dto import ListCustomersQuery
from saas_o_matic.application.customers.queries import CustomerQueries
from saas_o_matic.application.pagination import InvalidQueryData
from saas_o_matic.application.simulations.dto import SimulationHistoryQuery
from saas_o_matic.application.simulations.queries import SimulationQueries
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.simulations.entities import Simulation


class ReadCustomers:
    def __init__(self) -> None:
        self.search: str | None = "unset"
        self.called = False

    def exists_by_id(self, customer_id: UUID) -> bool:
        return True

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        return None

    def list_page(
        self, *, search: str | None, limit: int, offset: int
    ) -> tuple[list[Customer], int]:
        self.called = True
        self.search = search
        return [], 0


class ReadSimulations:
    def __init__(self) -> None:
        self.called = False

    def list_for_customer(
        self, customer_id: UUID, *, limit: int, offset: int
    ) -> tuple[list[Simulation], int]:
        self.called = True
        return [], 0


@pytest.mark.parametrize(
    "limit,offset", [(0, 0), (101, 0), (True, 0), (1, -1), (1, False), ("20", 0), (1, 1.5)]
)
def test_application_defensive_pagination(limit: object, offset: object) -> None:
    customers = ReadCustomers()
    simulations = ReadSimulations()
    with pytest.raises(InvalidQueryData):
        CustomerQueries(customers).list(
            ListCustomersQuery(limit=cast(Any, limit), offset=cast(Any, offset))
        )
    with pytest.raises(InvalidQueryData):
        SimulationQueries(customers=customers, simulations=simulations).history(
            SimulationHistoryQuery(UUID(int=1), limit=cast(Any, limit), offset=cast(Any, offset))
        )
    assert not customers.called and not simulations.called


@pytest.mark.parametrize(
    "search,expected", [("  acme  ", "acme"), ("   ", None), ("", None), (None, None)]
)
def test_application_normalizes_search(search: str | None, expected: str | None) -> None:
    repository = ReadCustomers()
    CustomerQueries(repository).list(ListCustomersQuery(search))
    assert repository.search == expected


def test_application_rejects_long_search() -> None:
    repository = ReadCustomers()
    with pytest.raises(InvalidQueryData):
        CustomerQueries(repository).list(ListCustomersQuery("x" * 256))
    assert not repository.called
