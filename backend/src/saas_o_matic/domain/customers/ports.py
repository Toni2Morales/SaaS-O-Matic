"""Puertos del dominio de clientes."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import CountryCode, TaxId


class CustomerQueryRepository(Protocol):
    """Lecturas paginadas; separado del puerto de creación y cálculo."""

    def get_by_id(self, customer_id: UUID) -> Customer | None: ...

    def exists_by_id(self, customer_id: UUID) -> bool: ...

    def list_page(
        self,
        *,
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Customer], int]: ...


class CustomerRepository(Protocol):
    """Puerto de persistencia para clientes."""

    def exists_by_tax_id(self, tax_id: TaxId, country: CountryCode) -> bool:
        """Comprueba si ya existe el identificador fiscal normalizado en el país."""

    def exists_by_id(self, customer_id: UUID) -> bool:
        """Comprueba si existe un cliente por su identificador."""

    def get_country_by_id(self, customer_id: UUID) -> CountryCode | None:
        """Obtiene país para calcular; finaliza lectura antes de cualquier I/O externo."""

    def add(self, customer: Customer) -> None:
        """Persiste el cliente y confirma la transacción.

        La implementación concreta debe traducir los conflictos de unicidad de
        la base de datos a ``DuplicateCustomerTaxId``.
        """
