from src.domain import (User, 
                        Order, 
                        Clothes, 
                        LaundryBag, 
                        Machine, 
                        MachineState,
                        LaundryLabel,
                        ClothesState, 
                        OrderState)

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Interval, Enum
from sqlalchemy.orm import mapper, relationship
from .setup import metadata


users = Table(
    'user', 
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('address', String(255)), # TODO : validate?
    Column('userid', String(255))
)


orders = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    # Column('clothes_list', ForeignKey('clothes.id')),
    Column('userid', String(255), ForeignKey('user.id')),
    Column('received_at', Date, nullable = True),
    Column('status', Enum(OrderState)),
    Column('orderid', String(255)),
)

clothes = Table(
    'clothes',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('clothesid', String(255)),
    Column('label', Enum(LaundryLabel)),
    Column('orderid', String(255), ForeignKey('order.orderid')),
    Column('status', Enum(ClothesState)),
    Column('received_at', Date)
)

laundrybags = Table(
    'laundrybag',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('clothesid', ForeignKey('clothes.id')),
    Column('created_at', Date),
    Column('label', Enum(LaundryLabel)),
)

machines = Table(
    'machine',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('machineid', String(255)),
    # Column('contained', ForeignKey('laundrybag.id')),
    Column('start_time', Date, nullable = True),
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
                         properties={'orders' : relationship(Order, backref = 'user')}
                        )
    clothes_mapper = mapper(Clothes, clothes)
    laundrybag_mapper = mapper(LaundryBag, 
                               laundrybags,
                               properties= {'clothes' : relationship(Clothes, backref = 'laundrybag')}
                                )
    machine_mapper = mapper(Machine, 
                            machines,
                            properties = {'contained' : relationship(LaundryBag, backref = 'machine', uselist = False)}
                            )
