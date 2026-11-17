"""Modelo de persistencia de simulaciones."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from saas_o_matic.infrastructure.database import Base


class SimulationModel(Base):
    """Tabla de simulaciones con su subtotal histórico exacto."""

    __tablename__ = "simulations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("customers.id", name="fk_simulations_customer_id"),
        nullable=False,
    )
    user_count: Mapped[int] = mapped_column(Integer, nullable=False)
    user_subtotal_eur: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "user_count >= 1 AND user_count <= 1000000",
            name="ck_simulations_user_count_range",
        ),
    )
