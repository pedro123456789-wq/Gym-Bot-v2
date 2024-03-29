"""empty message

Revision ID: b9890feb9e5b
Revises: 2549d017b2bf
Create Date: 2022-06-11 17:27:49.184805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9890feb9e5b'
down_revision = '2549d017b2bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise', sa.Column('name', sa.Text(), nullable=True))
    op.alter_column('run', 'userId',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('run', 'userId',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('exercise', 'name')
    # ### end Alembic commands ###
