from .clothes import Clothes, ClothesState
from src.domain.base import Base

from enum import Enum
from typing import List, Optional
from datetime import datetime


import sqlalchemy
from sqlalchemy import orm, select, func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, type_coerce

class OrderState(str, Enum) :
    CANCELLED = '취소'
    SENDING = '이동중'
    PREPARING = '준비중'
    WASHING = '세탁중'
    RECLAIMING = '정리중'
    SHIP_READY = '배송준비완료'
    SHIPPING = '배송중'
    DONE = '완료'




def clothes_order_mapping(clothes_status) : 
    orderstate = OrderState.CANCELLED
    if  clothes_status is None :
        return orderstate
    
    if clothes_status == ClothesState.CANCELLED :
        orderstate = OrderState.CANCELLED
    elif clothes_status == ClothesState.PREPARING :
        orderstate = OrderState.SENDING                    
    elif clothes_status == ClothesState.DISTRIBUTED :
        orderstate = OrderState.PREPARING
    elif clothes_status == ClothesState.PROCESSING :
        orderstate = OrderState.WASHING
    elif clothes_status == ClothesState.STOPPED :
        orderstate = OrderState.WASHING
    elif clothes_status == ClothesState.DONE :
        orderstate = OrderState.RECLAIMING
    elif clothes_status == ClothesState.RECLAIMED :
        orderstate = OrderState.SHIP_READY
    return orderstate






class Order(Base):
    # TODO [Order] order should only be generated from user.
    # TODO : [Order] received time by each status?
    __tablename__ = 'order'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    orderid = Column('orderid', String(20), unique = True)
    userid = Column('userid', String(20), ForeignKey('user.id'), nullable = True) # userid reference 방법?
    status = Column('status', sqlalchemy.Enum(OrderState), default = OrderState.SENDING)
    clothes_list = relationship('Clothes', backref = 'order')
    received_at = Column('received_at', DateTime, nullable = True)
    
    def __init__(self, 
                 orderid : str,
                 userid : str = None,
                 clothes_list : List[Clothes] = [],
                 received_at : Optional[datetime] = None, 
                 status : OrderState = OrderState.SENDING ) :
        self.userid = userid
        self.orderid = orderid
        self.clothes_list = clothes_list
        self.received_at = received_at
        self._status = status
    

        for clothes in self.clothes_list :
            clothes.orderid = self.orderid
            # clothes.status = ClothesState.PREPARING
            clothes.received_at = self.received_at

    def update_status(self) -> None :
        clothes_state = max((clothes.status for clothes in self.clothes_list)) if self.clothes_list else None # max returns the earliest ClothesState of clothes_list
        self._status = clothes_order_mapping(clothes_state)
        
    # return clothes_order_mapping(clothes_state)
    def update_status_by_clothes(self) :
        clothes_state = max((clothes.status for clothes in self.clothes_list)) if self.clothes_list else None # max returns the earliest ClothesState of clothes_list
        self._status = clothes_order_mapping(clothes_state)

    @property
    def volume(self) -> float :
        return sum(clothes.volume for clothes in self.clothes_list)

    def __repr__(self) :
        return f'[Order id=<{self.orderid}>, #clothes={len(self.clothes_list)}, status={self.status} ]'