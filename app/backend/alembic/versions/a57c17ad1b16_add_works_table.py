"""add_works_table

Revision ID: a57c17ad1b16
Revises: c4632c1b466e
Create Date: 2026-11-21 17:13:39.146174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a57c17ad1b16'
down_revision: Union[str, Sequence[str], None] = 'c4632c1b466e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "works",
        sa.Column("id", sa.Uuid(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("car_id", sa.Uuid(), sa.ForeignKey("cars.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("cost", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("performed_date", sa.Date(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("works")
