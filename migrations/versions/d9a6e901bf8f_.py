"""empty message

Revision ID: d9a6e901bf8f
Revises: 
Create Date: 2020-11-28 19:03:57.377420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a6e901bf8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_node_name'), 'node', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('leaf',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaf_end'), 'leaf', ['end'], unique=False)
    op.create_index(op.f('ix_leaf_name'), 'leaf', ['name'], unique=True)
    op.create_index(op.f('ix_leaf_start'), 'leaf', ['start'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leaf_start'), table_name='leaf')
    op.drop_index(op.f('ix_leaf_name'), table_name='leaf')
    op.drop_index(op.f('ix_leaf_end'), table_name='leaf')
    op.drop_table('leaf')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_node_name'), table_name='node')
    op.drop_table('node')
    # ### end Alembic commands ###