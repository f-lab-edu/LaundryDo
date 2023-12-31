from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from .clothes import Clothes, ClothesState, LaundryLabel

from enum import Enum
from typing import List, Optional
from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime

from src.domain.base import Base


class MaximumVolumeExceedError(Exception) :
    pass

class LaundryBagState(str, Enum) :
    COLLECTING = '수거중'
    READY = '세탁준비'
    RUNNING = '세탁중'
    DONE = '세탁완료'
    OBSOLETE = '더이상사용안함' ## TODO how to handle when laundrybag is out of machine and done laundrying.



class LaundryBag(Base):
    
    __tablename__ = 'laundrybag'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    laundrybagid = Column('laundrybagid', String(255), unique = True)
    status = Column('status', sqlalchemy.Enum(LaundryBagState), default = LaundryBagState.COLLECTING)
    # Column('clothesid', ForeignKey('clothes.id')),
    machineid = Column('machineid', ForeignKey('machine.id'), nullable = True)
    created_at = Column('created_at', DateTime, default = datetime.now())
    label = Column('label', sqlalchemy.Enum(LaundryLabel), default = LaundryLabel.UNDEFINED)
    clothes_list = relationship('Clothes', backref = 'laundrybag')

   
    def __init__(self, laundrybagid,  status = LaundryBagState.COLLECTING, clothes_list = []) : 
        ## TODO : [LaundryBag] if clothes does not have orderid, it cannot be in laundrybag
        self.laundrybagid = laundrybagid
        self.created_at = datetime.now()
        self.status = status
        self.clothes_list = clothes_list
        

        # TODO remove this
        for clothes in self.clothes_list :
            clothes.status = ClothesState.DISTRIBUTED
        

    def can_contain(self, clothes : Clothes) :
        return self.volume + clothes.volume <= LAUNDRYBAG_MAXVOLUME and (self.label is None or self.label == clothes.label)

    def append(self, clothes) :
        if self.can_contain(clothes) and self.status == LaundryBagState.COLLECTING :
            clothes.status = ClothesState.DISTRIBUTED
            if not self.label :
                self.label = clothes.label

            self.clothes_list.append(clothes)
            if self.volume >= LAUNDRYBAG_MAXVOLUME :
                self.status = LaundryBagState.READY


    @property
    def volume(self):
        if self.clothes_list :
            return sum(clothes.volume for clothes in self.clothes_list)
        else :
            return 0


    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.created_at < other.created_at
        else:
            raise TypeError(
                f"{type(other)} cannot be compared with {self.__class__} class."
            )

    def __repr__(self) :
        return f'<laundrybag id={self.laundrybagid}, 부피:{self.volume}|라벨:{self.label}|옷감:{self.clothes_list}>'