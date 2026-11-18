"""Composición del módulo de clientes.

El composition root construye el caso de uso con el repositorio SQLAlchemy y una
sesión por petición HTTP.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from saas_o_matic.application.customers.queries import CustomerQueries
from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.infrastructure.customers.repositories import SqlAlchemyCustomerRepository


def build_customer_use_case(session: Session) -> CreateCustomer:
    """Construye el caso de uso de alta con su repositorio concreto."""

    return CreateCustomer(SqlAlchemyCustomerRepository(session))


def build_customer_queries(session: Session) -> CustomerQueries:
    return CustomerQueries(SqlAlchemyCustomerRepository(session))
