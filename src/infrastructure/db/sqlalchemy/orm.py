from src.domain import (User, 
                        Order, 
                        Clothes, 
                        LaundryBag, 
                        Machine, 
                        MachineState,
                        LaundryLabel,
                        ClothesState, 
                        OrderState)

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Interval, Enum, Index, ForeignKeyConstraint, Float
from sqlalchemy.orm import mapper, relationship

from src.domain.laundrybag import LaundryBagState
from .setup import metadata


users = Table(
    'user', 
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('address', String(255)), # TODO : validate?
    Column('userid', String(20))
)


orders = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('orderid', String(255)),
    Column('received_at', DateTime, nullable = True),
    Column('status', Enum(OrderState)),
    Column('userid', String(20), ForeignKey('user.userid')),
)

clothes = Table(
    'clothes',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('clothesid', String(255)),
    Column('label', Enum(LaundryLabel)),
    Column('volume', Float),
    Column('orderid', String(255), ForeignKey('order.orderid')),
    Column('laundrybagid', String(255), ForeignKey('laundrybag.laundrybagid')),
    Column('status', Enum(ClothesState)),
    Column('received_at', DateTime),
)


laundrybags = Table(
    'laundrybag',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('laundrybagid', String(255)),
    Column('status', Enum(LaundryBagState)),
    # Column('clothesid', ForeignKey('clothes.id')),
    Column('machineid', ForeignKey('machine.id'), nullable = True),
    Column('created_at', DateTime),
    Column('label', Enum(LaundryLabel)),
)

machines = Table(
    'machine',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('machineid', String(255)),
    # Column('laundrybagid', ForeignKey('laundrybag.id')),
    Column('start_time', DateTime, nullable = True),
    Column('runtime', Interval),
    Column('status', Enum(MachineState))
)





def start_mappers() :
    order_mapper = mapper(Order, 
                          orders,
                          properties = {'clothes_list' : relationship(Clothes, backref = 'order' )}
                         )
    user_mapper = mapper(User, 
                         users,
                         properties={'orderlist' : relationship(Order, backref = 'user')}
                        )
    clothes_mapper = mapper(Clothes, clothes)
    laundrybag_mapper = mapper(LaundryBag, 
                               laundrybags,
                               properties= {'clothes_list' : relationship(Clothes, backref = 'laundrybag')}
                                )
    machine_mapper = mapper(Machine, 
                            machines,
                            properties = {'contained' : relationship(LaundryBag, backref = 'machine', uselist = False)}
                            )
