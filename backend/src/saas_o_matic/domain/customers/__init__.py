"""Modelo de dominio de clientes."""

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import (
    CustomerDomainError,
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
    TaxIdKind,
)

__all__ = [
    "CountryCode",
    "Customer",
    "CustomerDomainError",
    "CustomerRepository",
    "DuplicateCustomerTaxId",
    "InvalidCountry",
    "InvalidLegalName",
    "InvalidPlan",
    "InvalidTaxId",
    "PlanCode",
    "SpanishTaxId",
    "TaxIdKind",
]
