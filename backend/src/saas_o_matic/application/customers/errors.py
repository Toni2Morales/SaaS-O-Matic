"""Errores de aplicación del módulo de clientes."""

from __future__ import annotations


class CustomerApplicationError(Exception):
    """Error base de la aplicación de clientes."""


class InvalidCustomerData(CustomerApplicationError):
    """Los datos del cliente no superan una validación de dominio."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(message)


class CustomerTaxIdAlreadyExists(CustomerApplicationError):
    """El identificador fiscal normalizado ya está registrado en el país."""

    def __init__(self, tax_id: str, country: str) -> None:
        self.tax_id = tax_id
        self.country = country
        super().__init__(
            f"Ya existe un cliente con el identificador fiscal {tax_id} para el país {country}."
        )
