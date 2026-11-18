"""Amplía clientes y simulaciones sin inventar consumos históricos."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_international_simulations"
down_revision: str | None = "0002_create_simulations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _check_foreign_keys() -> None:
    """Comprueba integridad incluso durante la reconstrucción batch de SQLite."""

    if op.get_bind().exec_driver_sql("PRAGMA foreign_key_check").fetchall():
        raise RuntimeError("La migración detectó claves foráneas inconsistentes.")


def upgrade() -> None:
    """Conserva los históricos y añade los consumos como desconocidos."""

    _check_foreign_keys()
    with op.batch_alter_table("customers") as batch:
        batch.alter_column("tax_id", existing_type=sa.String(9), type_=sa.String(64))
    with op.batch_alter_table("simulations") as batch:
        batch.drop_constraint("ck_simulations_user_count_range", type_="check")
        batch.create_check_constraint(
            "ck_simulations_user_count_range",
            "typeof(user_count) = 'integer' AND user_count BETWEEN 0 AND 1000000",
        )
        batch.add_column(sa.Column("storage_gb", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("api_calls_per_month", sa.Integer(), nullable=True))
        batch.add_column(
            sa.Column("billing_period", sa.String(7), nullable=False, server_default="monthly")
        )
        batch.create_check_constraint(
            "ck_simulations_storage_gb_range",
            "storage_gb IS NULL OR (typeof(storage_gb) = 'integer' "
            "AND storage_gb BETWEEN 0 AND 1000000)",
        )
        batch.create_check_constraint(
            "ck_simulations_api_calls_range",
            "api_calls_per_month IS NULL OR (typeof(api_calls_per_month) = 'integer' "
            "AND api_calls_per_month BETWEEN 0 AND 1000000000)",
        )
        batch.create_check_constraint("ck_simulations_billing_period", "billing_period = 'monthly'")
    _check_foreign_keys()


def downgrade() -> None:
    """Falla antes del DDL cuando revertir perdería datos o semántica aprobada."""

    bind = op.get_bind()
    incompatible_customers = bind.execute(
        sa.text("SELECT COUNT(*) FROM customers WHERE country != 'ES' OR length(tax_id) > 9")
    ).scalar_one()
    incompatible_simulations = bind.execute(
        sa.text(
            "SELECT COUNT(*) FROM simulations WHERE user_count = 0 "
            "OR storage_gb IS NOT NULL OR api_calls_per_month IS NOT NULL"
        )
    ).scalar_one()
    if incompatible_customers or incompatible_simulations:
        raise RuntimeError(
            "Downgrade bloqueado: existen datos incompatibles o consumos que se perderían."
        )
    _check_foreign_keys()
    with op.batch_alter_table("simulations") as batch:
        for name in ("storage_gb_range", "api_calls_range", "billing_period", "user_count_range"):
            batch.drop_constraint(f"ck_simulations_{name}", type_="check")
        for name in ("storage_gb", "api_calls_per_month", "billing_period"):
            batch.drop_column(name)
        batch.create_check_constraint(
            "ck_simulations_user_count_range", "user_count >= 1 AND user_count <= 1000000"
        )
    with op.batch_alter_table("customers") as batch:
        batch.alter_column("tax_id", existing_type=sa.String(64), type_=sa.String(9))
    _check_foreign_keys()
