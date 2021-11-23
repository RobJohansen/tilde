"""empty message

Revision ID: ee6d41c353d2
Revises: 227777ff6e80
Create Date: 2021-11-23 15:26:44.566825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee6d41c353d2'
down_revision = '227777ff6e80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('node_term', sa.Column('name', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_node_term_name'), 'node_term', ['name'], unique=True)
    op.drop_index('ix_node_term_term', table_name='node_term')
    op.drop_column('node_term', 'term')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('node_term', sa.Column('term', sa.VARCHAR(length=64), nullable=True))
    op.create_index('ix_node_term_term', 'node_term', ['term'], unique=1)
    op.drop_index(op.f('ix_node_term_name'), table_name='node_term')
    op.drop_column('node_term', 'name')
    # ### end Alembic commands ###
