"""Repositorio SQLAlchemy de clientes."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import DuplicateCustomerTaxId
from saas_o_matic.domain.customers.value_objects import CountryCode, TaxId
from saas_o_matic.infrastructure.customers.mappers import to_domain, to_model
from saas_o_matic.infrastructure.customers.models import CustomerModel


class SqlAlchemyCustomerRepository:
    """Implementación concreta del puerto de clientes sobre SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def exists_by_tax_id(self, tax_id: TaxId, country: CountryCode) -> bool:
        """Comprueba la existencia del identificador fiscal normalizado en el país."""

        statement = select(CustomerModel.id).where(
            CustomerModel.tax_id == tax_id.value,
            CustomerModel.country == country.value,
        )
        return self._session.scalar(statement) is not None

    def exists_by_id(self, customer_id: UUID) -> bool:
        """Comprueba si existe un cliente por su identificador."""

        statement = select(CustomerModel.id).where(CustomerModel.id == customer_id)
        with self._session.no_autoflush:
            return self._session.scalar(statement) is not None

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        with self._session.no_autoflush:
            model = self._session.get(CustomerModel, customer_id)
            return to_domain(model) if model is not None else None

    def list_page(
        self,
        *,
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Customer], int]:
        """COUNT y página en SQLite, patrón parametrizado con literales LIKE."""

        statement = select(CustomerModel)
        count = select(func.count()).select_from(CustomerModel)
        if search:
            literal = (
                search.casefold().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            )
            pattern = f"%{literal}%"
            predicate = or_(
                func.unicode_casefold(CustomerModel.legal_name).like(pattern, escape="\\"),
                func.unicode_casefold(CustomerModel.tax_id).like(pattern, escape="\\"),
            )
            statement = statement.where(predicate)
            count = count.where(predicate)
        with self._session.no_autoflush:
            total = self._session.scalar(count) or 0
            if offset >= total:
                return [], total
            models = self._session.scalars(
                statement.order_by(
                    func.unicode_casefold(CustomerModel.legal_name).asc(),
                    CustomerModel.id.asc(),
                )
                .limit(limit)
                .offset(offset)
            ).all()
            return [to_domain(model) for model in models], total

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

    def get_country_by_id(self, customer_id: UUID) -> CountryCode | None:
        """Lectura inicial del caso de uso, sin escrituras pendientes en esta sesión."""

        with self._session.no_autoflush:
            value = self._session.scalar(
                select(CustomerModel.country).where(CustomerModel.id == customer_id)
            )
        self._session.rollback()
        return CountryCode.parse(value) if value is not None else None


def _is_unique_violation(error: IntegrityError) -> bool:
    """Detecta un conflicto de unicidad sin exponer el error de SQLAlchemy."""

    return "unique" in str(error.orig).lower()
