"""Errores de dominio del módulo de precios."""


class PricingDomainError(Exception):
    """Error base del dominio de precios."""


class InvalidUserCount(PricingDomainError):
    """El número de usuarios no es un entero no negativo válido."""

    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__("El número de usuarios debe ser un entero no negativo.")


class InvalidPricingSchedule(PricingDomainError):
    """La configuración de tramos no cumple las invariantes del motor."""
