"""Initial Migration

Revision ID: 843d1c18f16e
Revises: 
Create Date: 2023-12-19 03:20:00.015904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843d1c18f16e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favourite_color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('favourite_color')

    # ### end Alembic commands ###
