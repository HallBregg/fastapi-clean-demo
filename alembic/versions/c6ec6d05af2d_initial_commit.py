"""Initial commit.

Revision ID: c6ec6d05af2d
Revises: 
Create Date: 2022-12-17 16:42:16.541034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ec6d05af2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('primary_author', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('book')
