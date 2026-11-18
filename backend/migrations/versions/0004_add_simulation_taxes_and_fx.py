"""Añade snapshots exactos sin recalcular datos históricos."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_add_simulation_taxes_and_fx"
down_revision: str | None = "0003_international_simulations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("simulations", sa.Column("calculation_snapshot", sa.Text(), nullable=True))


def downgrade() -> None:
    if (
        op.get_bind()
        .execute(sa.text("SELECT COUNT(*) FROM simulations WHERE calculation_snapshot IS NOT NULL"))
        .scalar_one()
    ):
        raise RuntimeError("Downgrade bloqueado: se perderían snapshots fiscales y de divisas.")
    with op.batch_alter_table("simulations") as batch:
        batch.drop_column("calculation_snapshot")
    if op.get_bind().exec_driver_sql("PRAGMA foreign_key_check").fetchall():
        raise RuntimeError("Integridad referencial inconsistente.")
