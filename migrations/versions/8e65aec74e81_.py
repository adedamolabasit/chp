"""empty message

Revision ID: 8e65aec74e81
Revises: edfc09b6a13e
Create Date: 2022-04-12 20:06:40.398416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e65aec74e81'
down_revision = 'edfc09b6a13e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password1', sa.Text(), nullable=True),
    sa.Column('password2', sa.Text(), nullable=True),
    sa.Column('permission', sa.Boolean(), nullable=True),
    sa.Column('super_permission', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('confirm_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('company_email', sa.String(length=50), nullable=True),
    sa.Column('company_name', sa.String(length=50), nullable=True),
    sa.Column('company_region', sa.String(length=50), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('branch1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('tree_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tree_id'], ['tree.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('branch2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('branch1_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['branch1_id'], ['branch1.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('main', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('branch2_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['branch2_id'], ['branch2.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('parent', 'select')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parent', sa.Column('select', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_table('answer')
    op.drop_table('branch2')
    op.drop_table('branch1')
    op.drop_table('tree')
    op.drop_table('confirm_user')
    op.drop_table('admin_user')
    # ### end Alembic commands ###