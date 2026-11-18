"""Conversión entre el modelo de persistencia y la entidad de dominio."""

from __future__ import annotations

from datetime import UTC

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.value_objects import CountryCode, PlanCode, parse_tax_id
from saas_o_matic.infrastructure.customers.models import CustomerModel


def to_domain(model: CustomerModel) -> Customer:
    """Convierte una fila persistida en la entidad de dominio."""

    created_at = model.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    return Customer(
        id=model.id,
        legal_name=model.legal_name,
        tax_id=parse_tax_id(model.tax_id, CountryCode.parse(model.country)),
        email=model.email,
        country=CountryCode.parse(model.country),
        plan=PlanCode.parse(model.plan),
        created_at=created_at,
    )


def to_model(customer: Customer) -> CustomerModel:
    """Convierte una entidad de dominio en su modelo de persistencia."""

    return CustomerModel(
        id=customer.id,
        legal_name=customer.legal_name,
        tax_id=customer.tax_id.value,
        email=customer.email,
        country=customer.country.value,
        plan=customer.plan.value,
        created_at=customer.created_at,
    )
