"""added token column

Revision ID: 7d3dc24eab71
Revises: 893e515b38f1
Create Date: 2025-08-02 13:25:49.938886
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d3dc24eab71'
down_revision: Union[str, Sequence[str], None] = '893e515b38f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ⚠️ Do NOT add the column again, it's already present
    # op.add_column('orders', sa.Column('token_number', sa.Integer(), nullable=True))

    # Populate existing rows if they have NULL token_number
    op.execute("""
        UPDATE orders
        SET token_number = sub.token
        FROM (
            SELECT id, ROW_NUMBER() OVER (ORDER BY created_datetime ASC) AS token
            FROM orders
            WHERE token_number IS NULL
        ) AS sub
        WHERE orders.id = sub.id
    """)

    # Make the column non-nullable
    op.alter_column('orders', 'token_number', nullable=False)

    # Create index for token_number
    op.create_index(op.f('ix_orders_token_number'), 'orders', ['token_number'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_orders_token_number'), table_name='orders')
    op.drop_column('orders', 'token_number')
