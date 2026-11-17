"""Pruebas del caso de uso de alta de clientes."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from saas_o_matic.application.customers.dto import CreateCustomerCommand
from saas_o_matic.application.customers.errors import (
    CustomerTaxIdAlreadyExists,
    InvalidCustomerData,
)
from saas_o_matic.application.customers.use_cases import CreateCustomer
from saas_o_matic.domain.customers.entities import Customer
from saas_o_matic.domain.customers.errors import DuplicateCustomerTaxId, InvalidLegalName
from saas_o_matic.domain.customers.value_objects import CountryCode, PlanCode, SpanishTaxId

STANDARD_PLAN = PlanCode.STANDARD.value


class InMemoryCustomerRepository:
    """Repositorio de prueba que no depende de SQLAlchemy."""

    def __init__(self) -> None:
        self.customers: list[Customer] = []
        self.raise_duplicate_on_add = False

    def exists_by_tax_id(self, tax_id: SpanishTaxId, country: CountryCode) -> bool:
        return any(
            customer.tax_id.value == tax_id.value and customer.country is country
            for customer in self.customers
        )

    def exists_by_id(self, customer_id: UUID) -> bool:
        return any(customer.id == customer_id for customer in self.customers)

    def add(self, customer: Customer) -> None:
        if self.raise_duplicate_on_add:
            raise DuplicateCustomerTaxId(customer.tax_id.value, customer.country.value)
        self.customers.append(customer)


def _command(**overrides: str) -> CreateCustomerCommand:
    values = {
        "legal_name": "Cliente de prueba",
        "tax_id": " 12345678-z ",
        "email": "cliente@example.com",
        "country": "ES",
        "plan": STANDARD_PLAN,
    }
    values.update(overrides)
    return CreateCustomerCommand(**values)


def test_create_customer_normalizes_tax_id_and_returns_result() -> None:
    """El alta normaliza el identificador y genera UUID y fecha UTC."""

    repository = InMemoryCustomerRepository()
    result = CreateCustomer(repository).execute(_command())

    assert result.tax_id == "12345678Z"
    assert result.country is CountryCode.ES
    assert result.plan is PlanCode.STANDARD
    assert isinstance(result.id, UUID)
    assert result.created_at.tzinfo is UTC
    assert len(repository.customers) == 1


def test_create_customer_normalizes_legal_name() -> None:
    """El caso de uso recorta la razón social y conserva los espacios interiores."""

    repository = InMemoryCustomerRepository()
    result = CreateCustomer(repository).execute(_command(legal_name="  Empresa  Ejemplo S.L.  "))

    assert result.legal_name == "Empresa  Ejemplo S.L."
    assert repository.customers[0].legal_name == "Empresa  Ejemplo S.L."


@pytest.mark.parametrize("legal_name", ["", "   ", "X" * 256])
def test_create_customer_rejects_invalid_legal_name(legal_name: str) -> None:
    """Una razón social vacía o demasiado larga no llega al repositorio."""

    repository = InMemoryCustomerRepository()

    with pytest.raises(InvalidCustomerData) as error:
        CreateCustomer(repository).execute(_command(legal_name=legal_name))

    assert error.value.field == "legal_name"
    assert repository.customers == []


def test_create_customer_accepts_legal_name_with_255_characters() -> None:
    """La longitud máxima se aplica después del recorte."""

    repository = InMemoryCustomerRepository()
    result = CreateCustomer(repository).execute(_command(legal_name="X" * 255))

    assert result.legal_name == "X" * 255
    assert repository.customers[0].legal_name == "X" * 255


def test_customer_entity_normalizes_legal_name() -> None:
    """La entidad protege también las llamadas internas que no pasan por la API."""

    customer = Customer(
        id=uuid4(),
        legal_name="  Empresa  Ejemplo  ",
        tax_id=SpanishTaxId.parse("12345678Z"),
        email="cliente@example.com",
        country=CountryCode.ES,
        plan=PlanCode.STANDARD,
        created_at=datetime.now(UTC),
    )

    assert customer.legal_name == "Empresa  Ejemplo"


@pytest.mark.parametrize("legal_name", ["", "   ", "X" * 256])
def test_customer_entity_rejects_invalid_legal_name(legal_name: str) -> None:
    """La entidad rechaza razones sociales vacías o demasiado largas."""

    with pytest.raises(InvalidLegalName):
        Customer(
            id=uuid4(),
            legal_name=legal_name,
            tax_id=SpanishTaxId.parse("12345678Z"),
            email="cliente@example.com",
            country=CountryCode.ES,
            plan=PlanCode.STANDARD,
            created_at=datetime.now(UTC),
        )


def test_create_customer_rejects_invalid_tax_id() -> None:
    """Un identificador fiscal inválido se traduce a un error de aplicación."""

    repository = InMemoryCustomerRepository()

    with pytest.raises(InvalidCustomerData) as error:
        CreateCustomer(repository).execute(_command(tax_id="12345678A"))

    assert error.value.field == "tax_id"
    assert repository.customers == []


def test_create_customer_rejects_unsupported_country() -> None:
    """Un país no admitido se traduce a un error de aplicación."""

    repository = InMemoryCustomerRepository()

    with pytest.raises(InvalidCustomerData) as error:
        CreateCustomer(repository).execute(_command(country="FR"))

    assert error.value.field == "country"
    assert repository.customers == []


@pytest.mark.parametrize("plan", ["premium", "", "STANDARD"])
def test_create_customer_rejects_unsupported_plan(plan: str) -> None:
    """El plan debe pertenecer exactamente al catálogo aprobado."""

    repository = InMemoryCustomerRepository()

    with pytest.raises(InvalidCustomerData) as error:
        CreateCustomer(repository).execute(_command(plan=plan))

    assert error.value.field == "plan"
    assert repository.customers == []


def test_create_customer_rejects_duplicate_tax_id() -> None:
    """La comprobación previa impide un segundo alta con el mismo NIF."""

    repository = InMemoryCustomerRepository()
    use_case = CreateCustomer(repository)
    use_case.execute(_command())

    with pytest.raises(CustomerTaxIdAlreadyExists):
        use_case.execute(_command())


def test_create_customer_translates_repository_duplicate() -> None:
    """Un conflicto detectado al persistir también se traduce a la aplicación."""

    repository = InMemoryCustomerRepository()
    repository.raise_duplicate_on_add = True

    with pytest.raises(CustomerTaxIdAlreadyExists):
        CreateCustomer(repository).execute(_command())
