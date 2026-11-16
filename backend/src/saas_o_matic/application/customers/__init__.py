"""Aplicación del módulo de clientes."""

from saas_o_matic.application.customers.dto import CreateCustomerCommand, CustomerResult
from saas_o_matic.application.customers.errors import (
    CustomerApplicationError,
    CustomerTaxIdAlreadyExists,
    InvalidCustomerData,
)
from saas_o_matic.application.customers.use_cases import CreateCustomer

__all__ = [
    "CreateCustomer",
    "CreateCustomerCommand",
    "CustomerApplicationError",
    "CustomerResult",
    "CustomerTaxIdAlreadyExists",
    "InvalidCustomerData",
]
