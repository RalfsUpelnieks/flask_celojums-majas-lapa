"""reservation

Revision ID: f6ba7638547c
Revises: e777889222c4
Create Date: 2022-02-14 15:11:44.771391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6ba7638547c'
down_revision = 'e777889222c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], name=op.f('fk_reservation_trip_id_trip')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_reservation_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reservation'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')

    op.drop_table('reservation')
    # ### end Alembic commands ###