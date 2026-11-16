"""Infraestructura del módulo de clientes."""

from saas_o_matic.infrastructure.customers.models import CustomerModel
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository

__all__ = ["CustomerModel", "SqlAlchemyCustomerRepository"]
