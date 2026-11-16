"""Casos de uso del módulo de clientes."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from saas_o_matic.application.customers.dto import CreateCustomerCommand, CustomerResult
from saas_o_matic.application.customers.errors import (
    CustomerTaxIdAlreadyExists,
    InvalidCustomerData,
)
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import (
    DuplicateCustomerTaxId,
    InvalidCountry,
    InvalidLegalName,
    InvalidPlan,
    InvalidTaxId,
)
from saas_o_matic.domain.customers.ports import CustomerRepository
from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    PlanCode,
    SpanishTaxId,
    normalize_legal_name,
)


class CreateCustomer:
    """Caso de uso de alta de clientes.

    Valida el plan contra el catálogo aprobado del MVP, sin asignar valores por
    defecto. La persistencia y el commit quedan en el puerto de repositorio.
    """

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def execute(self, command: CreateCustomerCommand) -> CustomerResult:
        """Valida los datos, comprueba la unicidad fiscal y persiste el cliente."""

        try:
            legal_name = normalize_legal_name(command.legal_name)
        except InvalidLegalName as exc:
            raise InvalidCustomerData("legal_name", str(exc)) from exc

        try:
            tax_id = SpanishTaxId.parse(command.tax_id)
        except InvalidTaxId as exc:
            raise InvalidCustomerData("tax_id", str(exc)) from exc

        try:
            country = CountryCode.parse(command.country)
        except InvalidCountry as exc:
            raise InvalidCustomerData("country", str(exc)) from exc

        try:
            plan = PlanCode.parse(command.plan)
        except InvalidPlan as exc:
            raise InvalidCustomerData("plan", str(exc)) from exc

        if self._repository.exists_by_tax_id(tax_id, country):
            raise CustomerTaxIdAlreadyExists(tax_id.value, country.value)

        customer = Customer(
            id=uuid4(),
            legal_name=legal_name,
            tax_id=tax_id,
            email=command.email,
            country=country,
            plan=plan,
            created_at=datetime.now(UTC),
        )

        try:
            self._repository.add(customer)
        except DuplicateCustomerTaxId as exc:
            raise CustomerTaxIdAlreadyExists(tax_id.value, country.value) from exc

        return CustomerResult(
            id=customer.id,
            legal_name=customer.legal_name,
            tax_id=customer.tax_id.value,
            email=customer.email,
            country=customer.country,
            plan=customer.plan,
            created_at=customer.created_at,
        )
