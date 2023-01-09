"""Add link and tag tables.

Revision ID: 0952731fa83d
Revises: 
Create Date: 2022-12-26 19:51:56.369442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0952731fa83d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('primary_author', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('name', sa.String(), nullable=True),
    sa.UniqueConstraint('name')
    )
    op.create_table('link_tag',
    sa.Column('link_id', sa.BigInteger(), nullable=True),
    sa.Column('tag_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['link.id'], ),
    sa.ForeignKeyConstraint(['tag_name'], ['tag.name'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link_tag')
    op.drop_table('tag')
    op.drop_table('link')
    op.drop_table('book')
    # ### end Alembic commands ###