"""Crea la tabla de simulaciones.

Revision ID: 0002_create_simulations
Revises: 0001_create_customers
Create Date: 2026-11-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002_create_simulations"
down_revision: str | None = "0001_create_customers"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Crea la tabla ``simulations`` con sus restricciones."""

    op.create_table(
        "simulations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("user_count", sa.Integer(), nullable=False),
        sa.Column("user_subtotal_eur", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "user_count >= 1 AND user_count <= 1000000",
            name="ck_simulations_user_count_range",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name="fk_simulations_customer_id",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Elimina la tabla ``simulations``."""

    op.drop_table("simulations")
