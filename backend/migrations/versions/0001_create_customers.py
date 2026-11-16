"""Crea la tabla inicial de clientes.

Revision ID: 0001_create_customers
Revises:
Create Date: 2026-11-15

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_create_customers"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Crea la tabla ``customers`` con sus restricciones."""

    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("tax_id", sa.String(length=9), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("plan", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country", "tax_id", name="uq_customers_country_tax_id"),
    )


def downgrade() -> None:
    """Elimina la tabla ``customers``."""

    op.drop_table("customers")
