"""test

Revision ID: 1d198835dca8
Revises: 465a1ebb7ab8
Create Date: 2025-07-09 11:44:48.755882
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1d198835dca8'
down_revision: Union[str, Sequence[str], None] = '465a1ebb7ab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add the column as nullable with default fallback
    op.add_column(
        'cities',
        sa.Column('city_id', sa.String(), nullable=True, server_default='TEMP')
    )

    # Step 2: Remove server default so future inserts must specify city_id
    op.alter_column('cities', 'city_id', server_default=None)

    # Step 3 (Optional): You can later add NOT NULL constraint manually if needed
    # op.alter_column('cities', 'city_id', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cities', 'city_id')
