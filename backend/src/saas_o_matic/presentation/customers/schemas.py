"""Esquemas Pydantic de la API de clientes.

Los tipos de país y plan se reexportan desde aplicación para mantener una única
fuente de verdad en el dominio sin que presentación importe ``domain``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints

from saas_o_matic.application.customers.catalogs import (
    LEGAL_NAME_MAX_LENGTH,
    LEGAL_NAME_MIN_LENGTH,
    CountryCode,
    PlanCode,
)

LegalNameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=LEGAL_NAME_MIN_LENGTH,
        max_length=LEGAL_NAME_MAX_LENGTH,
    ),
]


class CustomerCreateRequest(BaseModel):
    """Datos de entrada del alta de un cliente."""

    legal_name: LegalNameStr
    tax_id: str
    email: EmailStr
    country: CountryCode
    plan: PlanCode


class CustomerResponse(BaseModel):
    """Representación de un cliente creado."""

    id: UUID
    legal_name: LegalNameStr
    tax_id: str
    email: EmailStr
    country: CountryCode
    plan: PlanCode
    created_at: datetime
