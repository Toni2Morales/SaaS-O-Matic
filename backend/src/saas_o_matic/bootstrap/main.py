"""Punto de entrada ASGI y composition root provisional."""

from saas_o_matic.presentation.app import create_app

app = create_app()
