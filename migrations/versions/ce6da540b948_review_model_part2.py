"""Review Model part2

Revision ID: ce6da540b948
Revises: 8b4bc6f3130f
Create Date: 2024-10-27 13:51:50.934527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce6da540b948'
down_revision = '8b4bc6f3130f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cleantype', sa.String(length=250), nullable=True))
        batch_op.drop_column('clean_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('clean_type', sa.VARCHAR(length=250), nullable=True))
        batch_op.drop_column('cleantype')

    # ### end Alembic commands ###