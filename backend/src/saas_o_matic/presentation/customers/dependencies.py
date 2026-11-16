"""Dependencias de presentación del módulo de clientes."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from saas_o_matic.application.customers.use_cases import CreateCustomer


def get_create_customer_use_case() -> CreateCustomer:
    """Dependencia sustituida por el composition root con el adaptador real."""

    raise RuntimeError("El caso de uso de clientes no está configurado.")


CreateCustomerUseCaseDep = Annotated[
    CreateCustomer,
    Depends(get_create_customer_use_case),
]
