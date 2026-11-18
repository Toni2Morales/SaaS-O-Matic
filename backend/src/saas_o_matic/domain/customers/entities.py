"""Entidades del dominio de clientes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from saas_o_matic.domain.customers.value_objects import (
    CountryCode,
    PlanCode,
    TaxId,
    normalize_legal_name,
)


@dataclass(frozen=True, slots=True)
class Customer:
    """Cliente con los datos aprobados de FR-01.

    ``plan`` pertenece al catálogo aprobado del MVP. No se asigna ningún valor
    por defecto ni se admiten planes fuera de ese catálogo.
    """

    id: UUID
    legal_name: str
    tax_id: TaxId
    email: str
    country: CountryCode
    plan: PlanCode
    created_at: datetime

    def __post_init__(self) -> None:
        """Normaliza la razón social para mantener la invariante de la entidad."""

        normalized = normalize_legal_name(self.legal_name)
        if normalized != self.legal_name:
            object.__setattr__(self, "legal_name", normalized)
