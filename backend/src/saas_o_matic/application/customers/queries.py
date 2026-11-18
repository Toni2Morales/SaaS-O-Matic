"""Lecturas de clientes sin efectos de escritura."""

from uuid import UUID

from saas_o_matic.application.customers.dto import (
    CustomerPageResult,
    CustomerResult,
    ListCustomersQuery,
)
from saas_o_matic.application.customers.errors import CustomerNotFound
from saas_o_matic.application.pagination import (
    MAX_SEARCH_LENGTH,
    InvalidQueryData,
    validate_pagination,
)
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.ports import CustomerQueryRepository


def customer_result(customer: Customer) -> CustomerResult:
    return CustomerResult(
        id=customer.id,
        legal_name=customer.legal_name,
        tax_id=customer.tax_id.value,
        email=customer.email,
        country=customer.country,
        plan=customer.plan,
        created_at=customer.created_at,
    )


class CustomerQueries:
    def __init__(self, repository: CustomerQueryRepository) -> None:
        self._repository = repository

    def get(self, customer_id: UUID) -> CustomerResult:
        customer = self._repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFound("El cliente solicitado no existe.")
        return customer_result(customer)

    def list(self, query: ListCustomersQuery) -> CustomerPageResult:
        validate_pagination(query.limit, query.offset)
        search = query.search.strip() if query.search is not None else None
        if search is not None and len(search) > MAX_SEARCH_LENGTH:
            raise InvalidQueryData(
                "search", f"Máximo {MAX_SEARCH_LENGTH} caracteres tras recortar."
            )
        customers, total = self._repository.list_page(
            search=search or None,
            limit=query.limit,
            offset=query.offset,
        )
        return CustomerPageResult(
            [customer_result(customer) for customer in customers],
            total,
            query.limit,
            query.offset,
        )
