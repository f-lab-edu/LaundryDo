from .spec import LAUNDRYBAG_MAXVOLUME
from .clothes import Clothes, ClothesState

from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class MaximumVolumeExceedError(Exception) :
    pass

class LaundryBagState(str, Enum) :
    COLLECTING = '수거중'
    READY = '세탁준비'
    RUN = '세탁중'
    DONE = '세탁완료'



class LaundryBag:
    
    __tablename__ = 'laundrybag'
    
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True), 
    Column('laundrybagid', String(255)),
    Column('status', Enum(LaundryBagState)),
    # Column('clothesid', ForeignKey('clothes.id')),
    Column('machineid', ForeignKey('machine.id'), nullable = True),
    Column('created_at', DateTime),
    Column('label', Enum(LaundryLabel)),


    def __init__(self, laundrybagid : str, clothes_list: List[Clothes] = [], created_at: datetime = None):
        ## TODO : [LaundryBag] if clothes does not have orderid, it cannot be in laundrybag
        self.laundrybagid = laundrybagid
        self.created_at = created_at
        self.status = LaundryBagState.COLLECTING
        self.clothes_list = clothes_list

        for clothes in clothes_list :
            clothes.status = ClothesState.DISTRIBUTED

    def can_contain(self, volume : float) :
        return self.volume + volume <= LAUNDRYBAG_MAXVOLUME

    def append(self, clothes) :
        if self.can_contain(clothes.volume) and self.status is LaundryBagState.COLLECTING :
            clothes.status = ClothesState.DISTRIBUTED
            self.clothes_list.append(clothes)
        else :
            self.status = LaundryBagState.READY
            raise MaximumVolumeExceedError

    @property
    def volume(self):
        return sum(clothes.volume for clothes in self.clothes_list)
        

    def update_clothes_status(self, status: ClothesState):
        [setattr(clothes, "status", status) for clothes in self.clothes_list]

    @property ## TODO : label is not recognized by sqlalchemy
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
        return f'<{self.laundrybagid}|무게:{self.volume}|라벨:{self.label}>'