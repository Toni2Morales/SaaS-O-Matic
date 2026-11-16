"""Repositorio SQLAlchemy de clientes."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import DuplicateCustomerTaxId
from saas_o_matic.domain.customers.value_objects import CountryCode, SpanishTaxId
from saas_o_matic.infrastructure.customers.mappers import to_model
from saas_o_matic.infrastructure.customers.models import CustomerModel


class SqlAlchemyCustomerRepository:
    """Implementación concreta del puerto de clientes sobre SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def exists_by_tax_id(self, tax_id: SpanishTaxId, country: CountryCode) -> bool:
        """Comprueba la existencia del identificador fiscal normalizado en el país."""

        statement = select(CustomerModel.id).where(
            CustomerModel.tax_id == tax_id.value,
            CustomerModel.country == country.value,
        )
        return self._session.scalar(statement) is not None

    def add(self, customer: Customer) -> None:
        """Persiste el cliente y confirma la transacción.

        La restricción única de base de datos sigue siendo la garantía final
        frente a duplicados concurrentes.
        """

        self._session.add(to_model(customer))
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            if _is_unique_violation(exc):
                raise DuplicateCustomerTaxId(customer.tax_id.value, customer.country.value) from exc
            raise


def _is_unique_violation(error: IntegrityError) -> bool:
    """Detecta un conflicto de unicidad sin exponer el error de SQLAlchemy."""

    return "unique" in str(error.orig).lower()
