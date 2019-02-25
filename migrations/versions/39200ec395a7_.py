"""empty message

Revision ID: 39200ec395a7
Revises: dd9723967dc0
Create Date: 2019-01-17 23:44:16.224000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39200ec395a7'
down_revision = 'dd9723967dc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('pwd', sa.String(length=100), nullable=True),
    sa.Column('is_super', sa.SmallInteger(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_admin_addtime'), 'admin', ['addtime'], unique=False)
    op.create_table('adminlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adminlog_addtime'), 'adminlog', ['addtime'], unique=False)
    op.create_table('oplog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('reason', sa.String(length=600), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oplog_addtime'), 'oplog', ['addtime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_oplog_addtime'), table_name='oplog')
    op.drop_table('oplog')
    op.drop_index(op.f('ix_adminlog_addtime'), table_name='adminlog')
    op.drop_table('adminlog')
    op.drop_index(op.f('ix_admin_addtime'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
