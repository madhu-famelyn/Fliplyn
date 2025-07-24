"""test

Revision ID: 8b726f2e0ec9
Revises: 1d198835dca8
Create Date: 2025-07-09 12:25:36.646051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b726f2e0ec9'
down_revision: Union[str, Sequence[str], None] = '1d198835dca8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add city_identifier column to buildings as nullable to avoid NotNullViolation
    op.add_column('buildings', sa.Column('city_identifier', sa.String(), nullable=True))

    # Keep city_id in cities as NOT NULL (already enforced earlier)
    op.alter_column('cities', 'city_id',
                    existing_type=sa.VARCHAR(),
                    nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('cities', 'city_id',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.drop_column('buildings', 'city_identifier')
