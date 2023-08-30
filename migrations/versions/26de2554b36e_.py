"""empty message

Revision ID: 26de2554b36e
Revises: 
Create Date: 2023-08-30 15:32:15.120453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26de2554b36e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('machine',
    sa.Column('machineid', sa.String(length=255), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('lastupdate_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('READY', 'STOP', 'RUNNING', 'DONE', 'BROKEN', name='machinestate'), nullable=True),
    sa.PrimaryKeyConstraint('machineid')
    )
    op.create_table('user',
    sa.Column('userid', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('userid')
    )
    op.create_table('laundrybag',
    sa.Column('laundrybagid', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('COLLECTING', 'READY', 'RUNNING', 'DONE', 'OBSOLETE', name='laundrybagstate'), nullable=True),
    sa.Column('machineid', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['machineid'], ['machine.machineid'], ),
    sa.PrimaryKeyConstraint('laundrybagid')
    )
    op.create_table('order',
    sa.Column('orderid', sa.String(length=255), nullable=False),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.Column('userid', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('orderid')
    )
    op.create_table('clothes',
    sa.Column('clothesid', sa.String(length=255), nullable=False),
    sa.Column('label', sa.Enum('WASH', 'DRY', 'HAND', name='laundrylabel'), nullable=True),
    sa.Column('volume', sa.Float(), nullable=True),
    sa.Column('orderid', sa.String(length=255), nullable=True),
    sa.Column('laundrybagid', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('CANCELLED', 'PREPARING', 'DISTRIBUTED', 'PROCESSING', 'STOPPED', 'DONE', 'RECLAIMED', name='clothesstate'), nullable=True),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['laundrybagid'], ['laundrybag.laundrybagid'], ),
    sa.ForeignKeyConstraint(['orderid'], ['order.orderid'], ),
    sa.PrimaryKeyConstraint('clothesid')
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
