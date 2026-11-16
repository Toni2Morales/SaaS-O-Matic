"""Catálogos de valores compartidos por la aplicación y la presentación.

La fuente de verdad sigue siendo el dominio. Este módulo permite que la capa de
presentación use los mismos tipos sin importar directamente ``domain``.
"""

from saas_o_matic.domain.customers.value_objects import (
    LEGAL_NAME_MAX_LENGTH,
    LEGAL_NAME_MIN_LENGTH,
    CountryCode,
    PlanCode,
)

__all__ = [
    "LEGAL_NAME_MAX_LENGTH",
    "LEGAL_NAME_MIN_LENGTH",
    "CountryCode",
    "PlanCode",
]
