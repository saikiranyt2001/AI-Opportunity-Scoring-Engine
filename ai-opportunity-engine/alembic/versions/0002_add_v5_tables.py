"""Add v5 feature tables

Revision ID: 0002_add_v5_tables
Revises: 0001_initial_schema
Create Date: 2026-03-22 00:30:00

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002_add_v5_tables"
down_revision: str | None = "0001_initial_schema"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "accessory_keywords",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("keyword", sa.String(length=255), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("source_model", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_accessory_keywords_product_id"), "accessory_keywords", ["product_id"], unique=False)
    op.create_index(op.f("ix_accessory_keywords_keyword"), "accessory_keywords", ["keyword"], unique=False)

    op.create_table(
        "shadow_model_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("models_responded", sa.Integer(), nullable=False),
        sa.Column("failures", sa.Integer(), nullable=False),
        sa.Column("average_score", sa.Float(), nullable=False),
        sa.Column("score_spread", sa.Float(), nullable=False),
        sa.Column("raw_payload", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_shadow_model_runs_product_id"), "shadow_model_runs", ["product_id"], unique=False)

    op.create_table(
        "alpha_beta_metrics",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("alpha_score", sa.Float(), nullable=False),
        sa.Column("beta_score", sa.Float(), nullable=False),
        sa.Column("oqs", sa.Float(), nullable=False),
        sa.Column("alpha_half_life_days", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alpha_beta_metrics_product_id"), "alpha_beta_metrics", ["product_id"], unique=False)

    op.create_table(
        "position_alerts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("criterion", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=30), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_position_alerts_product_id"), "position_alerts", ["product_id"], unique=False)
    op.create_index(op.f("ix_position_alerts_criterion"), "position_alerts", ["criterion"], unique=False)

    op.create_table(
        "patent_risk_flags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(length=30), nullable=False),
        sa.Column("rationale", sa.String(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patent_risk_flags_product_id"), "patent_risk_flags", ["product_id"], unique=False)
    op.create_index(op.f("ix_patent_risk_flags_risk_level"), "patent_risk_flags", ["risk_level"], unique=False)

    op.create_table(
        "digest_dispatches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("subscriber_email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("provider_message_id", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_digest_dispatches_subscriber_email"), "digest_dispatches", ["subscriber_email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_digest_dispatches_subscriber_email"), table_name="digest_dispatches")
    op.drop_table("digest_dispatches")

    op.drop_index(op.f("ix_patent_risk_flags_risk_level"), table_name="patent_risk_flags")
    op.drop_index(op.f("ix_patent_risk_flags_product_id"), table_name="patent_risk_flags")
    op.drop_table("patent_risk_flags")

    op.drop_index(op.f("ix_position_alerts_criterion"), table_name="position_alerts")
    op.drop_index(op.f("ix_position_alerts_product_id"), table_name="position_alerts")
    op.drop_table("position_alerts")

    op.drop_index(op.f("ix_alpha_beta_metrics_product_id"), table_name="alpha_beta_metrics")
    op.drop_table("alpha_beta_metrics")

    op.drop_index(op.f("ix_shadow_model_runs_product_id"), table_name="shadow_model_runs")
    op.drop_table("shadow_model_runs")

    op.drop_index(op.f("ix_accessory_keywords_keyword"), table_name="accessory_keywords")
    op.drop_index(op.f("ix_accessory_keywords_product_id"), table_name="accessory_keywords")
    op.drop_table("accessory_keywords")
