"""update columns

Revision ID: 0c818d0bdf5e
Revises: 4df6bcd15127
Create Date: 2024-10-22 14:49:27.450244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c818d0bdf5e'
down_revision = '4df6bcd15127'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('clean_package', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('date_of_service', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.drop_column('favorite_color')
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('favorite_color', sa.VARCHAR(length=120), nullable=True))
        batch_op.drop_column('amount')
        batch_op.drop_column('date_of_service')
        batch_op.drop_column('clean_package')

    # ### end Alembic commands ###
