"""test

Revision ID: dd62ba3d4ed6
Revises: bcaec706a005
Create Date: 2025-07-09 11:10:34.721417
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dd62ba3d4ed6'
down_revision: Union[str, Sequence[str], None] = 'bcaec706a005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add column as nullable
    op.add_column('states', sa.Column('state_id', sa.String(), nullable=True))

    # Step 2: Populate with dummy state_id values (e.g., "00001", "00002", ...)
    op.execute("""
        WITH numbered AS (
            SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS rn
            FROM states
        )
        UPDATE states
        SET state_id = LPAD(rn::text, 5, '0')
        FROM numbered
        WHERE states.id = numbered.id
    """)

    # Step 3: Alter column to NOT NULL
    op.alter_column('states', 'state_id', nullable=False)

    # Step 4: Add UNIQUE constraint
    op.create_unique_constraint('uq_states_state_id', 'states', ['state_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_states_state_id', 'states', type_='unique')
    op.drop_column('states', 'state_id')
