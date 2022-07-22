"""Add Transaction Fields

Revision ID: 38e24f3839ca
Revises: 5e8444053ce4
Create Date: 2022-07-22 13:27:43.151750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e24f3839ca'
down_revision = '5e8444053ce4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('fields', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'fields')
    # ### end Alembic commands ###
