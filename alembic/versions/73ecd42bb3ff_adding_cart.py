"""adding cart

Revision ID: 73ecd42bb3ff
Revises: 8b726f2e0ec9
Create Date: 2025-07-10 14:39:23.401135
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73ecd42bb3ff'
down_revision: Union[str, Sequence[str], None] = '8b726f2e0ec9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create 'carts' table
    op.create_table(
        'carts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('stall_id', sa.String(), nullable=False),
        sa.Column('created_datetime', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['stall_id'], ['stalls.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_carts_id'), 'carts', ['id'], unique=False)

    # Create 'cart_items' table
    op.create_table(
        'cart_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('cart_id', sa.String(), nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price_at_addition', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['cart_id'], ['carts.id']),
        sa.ForeignKeyConstraint(['item_id'], ['items.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_items_id'), 'cart_items', ['id'], unique=False)

    # ✅ Fix for NOT NULL city_identifier issue
    # Fill any null city_identifier values with a placeholder or default
    op.execute("UPDATE buildings SET city_identifier = 'UNKNOWN' WHERE city_identifier IS NULL")

    # Now it's safe to enforce NOT NULL
    op.alter_column('buildings', 'city_identifier',
               existing_type=sa.VARCHAR(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('buildings', 'city_identifier',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_cart_items_id'), table_name='cart_items')
    op.drop_table('cart_items')
    op.drop_index(op.f('ix_carts_id'), table_name='carts')
    op.drop_table('carts')
