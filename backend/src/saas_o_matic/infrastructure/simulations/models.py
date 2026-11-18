"""Modelo de persistencia de simulaciones."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, Uuid
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
    calculation_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    storage_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    api_calls_per_month: Mapped[int | None] = mapped_column(Integer, nullable=True)
    billing_period: Mapped[str] = mapped_column(
        String(7), nullable=False, default="monthly", server_default="monthly"
    )

    __table_args__ = (
        CheckConstraint(
            "typeof(user_count) = 'integer' AND user_count >= 0 AND user_count <= 1000000",
            name="ck_simulations_user_count_range",
        ),
        CheckConstraint(
            "storage_gb IS NULL OR (typeof(storage_gb) = 'integer' "
            "AND storage_gb BETWEEN 0 AND 1000000)",
            name="ck_simulations_storage_gb_range",
        ),
        CheckConstraint(
            "api_calls_per_month IS NULL OR (typeof(api_calls_per_month) = 'integer' "
            "AND api_calls_per_month BETWEEN 0 AND 1000000000)",
            name="ck_simulations_api_calls_range",
        ),
        CheckConstraint("billing_period = 'monthly'", name="ck_simulations_billing_period"),
    )
