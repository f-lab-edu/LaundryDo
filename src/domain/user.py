from .clothes import ClothesState
from .order import Order, OrderState
from src.domain.base import Base

from typing import List

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class User(Base) :

    __tablename__ = 'user'
    
    id = Column('id', Integer, primary_key = True, autoincrement = True)
    userid = Column('userid', String(20))
    password = Column('password', String(255), nullable = False)
    phone_number = Column('phone_number', String(20))
    address = Column('address', String(255))
    orderlist = relationship('Order', backref = 'user')

    def __init__(self, userid: str, address: str, password : str, phone_number : str, orderlist : List[Order] = []) :
        self.userid = userid
        self.password = password
        self.phone_number = phone_number
        self.address = address
        self.orderlist = orderlist


    def __repr__(self) :
        return f"[{self.__class__.__name__} id= {self.userid}, address= {self.address}]"

    
    def __hash__(self) :
        return hash(self.userid)

    def __eq__(self, other) :
        if self.__class__ == other.__class__ :
            return self.userid == other.userid
