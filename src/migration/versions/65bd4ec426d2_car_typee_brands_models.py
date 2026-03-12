"""car type/brands models

Revision ID: 65bd4ec426d2
Revises: ea0bd9d4903c
Create Date: 2026-02-17 01:20:32.218001
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "65bd4ec426d2"
down_revision: Union[str, Sequence[str], None] = "ea0bd9d4903c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ---- Create lookup tables ----
    op.create_table(
        "car_brands",
        sa.Column("car_brand_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("car_brand_name", sa.String(), nullable=False, unique=True),
    )

    op.create_table(
        "car_types",
        sa.Column("car_type_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("car_type_name", sa.String(), nullable=False, unique=True),
    )

    # ---- Drop old compatibility table (local only safe) ----
    op.drop_table("offer_car_compatibility")

    # ---- Recreate compatibility table cleanly ----
    op.create_table(
        "offer_car_compatibility",
        sa.Column(
            "offer_car_compatibility_id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "offer_id",
            sa.UUID(),
            sa.ForeignKey("offers.offer_id"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "car_type_id",
            sa.Integer(),
            sa.ForeignKey("car_types.car_type_id"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "car_brand_id",
            sa.Integer(),
            sa.ForeignKey("car_brands.car_brand_id"),
            nullable=False,
            index=True,
        ),
        sa.UniqueConstraint(
            "offer_id",
            "car_type_id",
            "car_brand_id",
            name="uq_offer_car_type_brand",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("offer_car_compatibility")
    op.drop_table("car_types")
    op.drop_table("car_brands")
