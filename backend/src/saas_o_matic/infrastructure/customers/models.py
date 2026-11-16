"""Modelo de persistencia de clientes."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from saas_o_matic.infrastructure.database import Base


class CustomerModel(Base):
    """Tabla de clientes.

    ``plan`` es obligatorio y pertenece al catálogo aprobado del MVP. La
    migración inicial refleja este mismo esquema.
    """

    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(9), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    plan: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (UniqueConstraint("country", "tax_id", name="uq_customers_country_tax_id"),)
