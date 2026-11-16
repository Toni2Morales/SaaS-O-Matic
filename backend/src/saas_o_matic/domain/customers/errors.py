"""Errores de dominio del módulo de clientes."""


class CustomerDomainError(Exception):
    """Error base del dominio de clientes."""


class InvalidLegalName(CustomerDomainError):
    """La razón social no cumple las reglas de contenido o longitud."""


class InvalidTaxId(CustomerDomainError):
    """El identificador fiscal no cumple el formato o el control esperado."""


class InvalidCountry(CustomerDomainError):
    """El país no está soportado por la primera versión."""


class InvalidPlan(CustomerDomainError):
    """El plan no pertenece al catálogo aprobado del MVP."""


class DuplicateCustomerTaxId(CustomerDomainError):
    """Ya existe un cliente con el identificador fiscal normalizado en el país."""

    def __init__(self, tax_id: str, country: str) -> None:
        self.tax_id = tax_id
        self.country = country
        super().__init__(
            f"Ya existe un cliente con el identificador fiscal {tax_id} para el país {country}."
        )
