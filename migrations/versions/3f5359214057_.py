"""empty message

Revision ID: 3f5359214057
Revises: 1af16c152bf1
Create Date: 2016-01-14 08:53:48.304326

"""

# revision identifiers, used by Alembic.
revision = '3f5359214057'
down_revision = '1af16c152bf1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('person_sum', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room')
    ### end Alembic commands ###
