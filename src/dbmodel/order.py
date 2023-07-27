from .clothes import Clothes
from .base import Base

from enum import Enum
from typing import List, Optional
from datetime import datetime


import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime


class OrderState(Enum) :
    CANCELLED = '취소'
    SENDING = '이동중'
    PREPARING = '준비중'
    WASHING = '세탁중'
    RECLAIMING = '정리중'
    SHIP_READY = '배송준비완료'
    SHIPPING = '배송중'
    DONE = '완료'

class Order(Base):
    # TODO : [Order] received time by each status?
    __tablename__ = 'order'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    orderid = Column('orderid', String(255))
    received_at = Column('received_at', DateTime, nullable = True)
    status = Column('status', sqlalchemy.Enum(OrderState))
    userid = Column('userid', String(20), ForeignKey('user.userid'))
    
    def __init__(self, 
                 userid : str,
                 orderid : str,
                 clothes_list : List[Clothes] = [],
                 received_at : Optional[datetime] = None,
                 status : OrderState = OrderState.SENDING) :
        self.userid = userid
        self.orderid = orderid
        self.clothes_list = clothes_list
        self.received_at = received_at
        self.status = status
    

        for clothes in self.clothes_list :
            clothes.orderid = self.orderid

    @property
    def volume(self) -> float :
        return sum(clothes.volume for clothes in self.clothes_list)

    def __repr__(self) :
        return f'Order <{self.orderid}>, {len(self.clothes_list)}, {self.status}'