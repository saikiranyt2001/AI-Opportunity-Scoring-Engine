"""Initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-03-22 00:00:00

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "pipeline_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pipeline_logs_event_type"), "pipeline_logs", ["event_type"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=True)

    op.create_table(
        "scores",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("primary_score", sa.Integer(), nullable=False),
        sa.Column("shadow_payload", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scores_product_id"), "scores", ["product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_scores_product_id"), table_name="scores")
    op.drop_table("scores")

    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_pipeline_logs_event_type"), table_name="pipeline_logs")
    op.drop_table("pipeline_logs")
