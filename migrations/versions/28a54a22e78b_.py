"""empty message

Revision ID: 28a54a22e78b
Revises: 
Create Date: 2023-10-28 19:27:20.568099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28a54a22e78b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('machine',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('machineid', sa.String(length=255), nullable=True),
    sa.Column('runtime', sa.Interval(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('lastupdate_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('READY', 'STOP', 'RUNNING', 'DONE', 'BROKEN', name='machinestate'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('machineid')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userid', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('laundrybag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('laundrybagid', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('COLLECTING', 'READY', 'RUNNING', 'DONE', 'OBSOLETE', name='laundrybagstate'), nullable=True),
    sa.Column('machineid', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('label', sa.Enum('UNDEFINED', 'WASH', 'DRY', 'HAND', name='laundrylabel'), nullable=True),
    sa.ForeignKeyConstraint(['machineid'], ['machine.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('laundrybagid')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('orderid', sa.String(length=20), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('CANCELLED', 'SENDING', 'PREPARING', 'WASHING', 'RECLAIMING', 'SHIP_READY', 'SHIPPING', 'DONE', name='orderstate'), nullable=True),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('orderid')
    )
    op.create_table('clothes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('clothesid', sa.String(length=255), nullable=True),
    sa.Column('label', sa.Enum('UNDEFINED', 'WASH', 'DRY', 'HAND', name='laundrylabel'), nullable=True),
    sa.Column('volume', sa.Float(), nullable=True),
    sa.Column('orderid', sa.Integer(), nullable=True),
    sa.Column('laundrybagid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('CANCELLED', 'PREPARING', 'DISTRIBUTED', 'PROCESSING', 'STOPPED', 'DONE', 'RECLAIMED', name='clothesstate'), nullable=True),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['laundrybagid'], ['laundrybag.id'], ),
    sa.ForeignKeyConstraint(['orderid'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('clothesid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clothes')
    op.drop_table('order')
    op.drop_table('laundrybag')
    op.drop_table('user')
    op.drop_table('machine')
    # ### end Alembic commands ###