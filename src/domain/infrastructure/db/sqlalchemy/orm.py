from src.domain import (User, 
                        Order, 
                        Clothes, 
                        LaundryBag, 
                        Machine, 
                        LaundryLabel,
                        ClothesState, 
                        OrderState)

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Interval, Enum
from sqlalchemy.orm import mapper, relationship
from .setup import metadata


users = Table(
    'users', 
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('address', String(255)), # TODO : validate?
    Column('userid', String(255))
)


orders = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('clothes_list', ForeignKey('clothes.id')),
    Column('received_at', Date, nullable = True),
    Column('status', Enum),
    Column('orderid', String(255))
)

clothes = Table(
    'clothes',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('label', Enum),
    Column('orderid', String(255), ForeignKey('orders.orderid')),
    Column('status', Enum),
    Column('received_at', Enum)
)

laundrybags = Table(
    'laundrybags',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('clothes_list', ForeignKey('clothes.id')),
    Column('created_at', Date),
    Column('label', Enum),
)

machines = Table(
    'machines',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('machineid', String(255)),
    Column('contained', ForeignKey('laundrybags.id')),
    Column('start_time', Date, nullable = True),
    Column('runtime', Interval),
    Column('status', Enum)
)



def start_mappers() :
    user_mapper = mapper(User, users)
    order_mapper = mapper(Order, orders)
    clothes_mapper = mapper(Clothes, clothes)
    laundrybag_mapper = mapper(LaundryBag, laundrybags)
    machine_mapper = mapper(Machine, machines)