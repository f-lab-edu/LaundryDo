from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from .clothes import Clothes, ClothesState, LaundryLabel

from enum import Enum
from typing import List, Optional
from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import declarative_base, relationship
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
    created_at = Column('created_at', DateTime)
    label = Column('label', sqlalchemy.Enum(LaundryLabel))
    clothes_list = relationship('Clothes', backref = 'laundrybag')

   
    def __init__(self, laundrybagid, created_at, status = LaundryBagState.COLLECTING, clothes_list = []) : 
        ## TODO : [LaundryBag] if clothes does not have orderid, it cannot be in laundrybag
        self.laundrybagid = laundrybagid
        self.created_at = created_at
        self.status = status
        self.clothes_list = clothes_list

        for clothes in self.clothes_list :
            clothes.status = ClothesState.DISTRIBUTED
        

    def can_contain(self, volume : float) :
        return self.volume + volume <= LAUNDRYBAG_MAXVOLUME

    def append(self, clothes) :
        if self.can_contain(clothes.volume) and self.status is LaundryBagState.COLLECTING :
            clothes.status = ClothesState.DISTRIBUTED
            self.clothes_list.append(clothes)
            if self.volume == LAUNDRYBAG_MAXVOLUME :
                self.status = LaundryBagState.READY
        else :
            self.status = LaundryBagState.READY
            
            # raise MaximumVolumeExceedError
    

    @property
    def volume(self):
        return sum(clothes.volume for clothes in self.clothes_list)
        

    def update_clothes_status(self, status: ClothesState):
        [setattr(clothes, "status", status) for clothes in self.clothes_list]

    @property 
    def label(self):
        return next((clothes.label for clothes in self.clothes_list), None)

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.created_at < other.created_at
        else:
            raise TypeError(
                f"{type(other)} cannot be compared with {self.__class__} class."
            )

    def __repr__(self) :
        return f'<laundrybag id={self.laundrybagid}, 무게:{self.volume}|라벨:{self.label}>'