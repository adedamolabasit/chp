"""empty message

Revision ID: 7179ff716c77
Revises: 9a2180776b40
Create Date: 2022-04-17 20:40:38.177876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7179ff716c77'
down_revision = '9a2180776b40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'branch2_id',
               existing_type=sa.INTEGER(),
               nullable='False')
    op.alter_column('branch1', 'tree_id',
               existing_type=sa.INTEGER(),
               nullable='False')
    op.alter_column('branch2', 'branch1_id',
               existing_type=sa.INTEGER(),
               nullable='False')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branch2', 'branch1_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('branch1', 'tree_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('answer', 'branch2_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
