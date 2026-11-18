"""DTOs del caso de uso de alta de clientes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from saas_o_matic.application.pagination import DEFAULT_PAGE_LIMIT
from saas_o_matic.domain.customers.value_objects import CountryCode, PlanCode


@dataclass(frozen=True, slots=True)
class CreateCustomerCommand:
    """Datos de entrada del alta.

    ``plan`` es obligatorio y se valida contra el catálogo aprobado del MVP.
    """

    legal_name: str
    tax_id: str
    email: str
    country: str
    plan: str


@dataclass(frozen=True, slots=True)
class CustomerResult:
    """Representación de salida de un cliente creado."""

    id: UUID
    legal_name: str
    tax_id: str
    email: str
    country: CountryCode
    plan: PlanCode
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ListCustomersQuery:
    search: str | None = None
    limit: int = DEFAULT_PAGE_LIMIT
    offset: int = 0


@dataclass(frozen=True, slots=True)
class CustomerPageResult:
    items: list[CustomerResult]
    total: int
    limit: int
    offset: int
