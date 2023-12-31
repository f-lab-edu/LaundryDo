from typing import Annotated, Optional
from enum import Enum
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime

from src.domain.base import Base


class ClothesState(str, Enum):
    CANCELLED = "취소"
    PREPARING = "준비중"
    DISTRIBUTED = "세탁전분류"  # 세탁 라벨에 따라 분류된 상태
    PROCESSING = "세탁중"
    STOPPED = "일시정지"  # 세탁기 고장이나 외부 요인으로 세탁 일시 중지
    DONE = "세탁완료"
    RECLAIMED = "세탁후분류"

class LaundryLabel(str, Enum):
    UNDEFINED = "미정"
    WASH = "물세탁"
    DRY = "드라이클리닝"
    HAND = "손세탁"


class Clothes(Base) :

    __tablename__ = 'clothes'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    clothesid = Column('clothesid', String(255), unique = True)
    label = Column('label', sqlalchemy.Enum(LaundryLabel), default = LaundryLabel.UNDEFINED)
    volume = Column('volume', Float)
    orderid = Column('orderid', Integer, ForeignKey('order.id'))
    laundrybagid = Column('laundrybagid', Integer, ForeignKey('laundrybag.id'), nullable = True)
    status = Column('status', sqlalchemy.Enum(ClothesState), default = ClothesState.PREPARING)
    received_at = Column('received_at', DateTime)

    def __init__(self, 
                clothesid : str, 
                label : LaundryLabel, 
                volume : float, 
                orderid: Optional[str] = None,
                laundrybagid : Optional[str] = None,
                status: ClothesState = ClothesState.PREPARING,
                received_at: Optional[datetime] = None ) :
        
        self.clothesid = clothesid
        self.label = label
        self.volume = volume
        self.orderid = orderid
        self.laundrybagid = laundrybagid
        self.status = status
        self.received_at = received_at
    
    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.received_at < other.received_at
        else:
            raise TypeError(f"{type(other)} cannot be compared with Clothes class.")
    
    def __hash__(self) :
        return hash(self.clothesid)
    
    def __eq__(self, other) :
        if isinstance(other.__class__, self.__class__) :
            return hash(self.clothesid) == hash(self.other)
        raise NotImplementedError
    
    def __repr__(self) :
        return f'[clothes id = {self.clothesid}, label = {self.label} orderid = {self.orderid}, status = {self.status}]'