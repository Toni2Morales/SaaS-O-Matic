"""DTOs del caso de uso de alta de clientes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

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
