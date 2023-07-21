from .spec import LAUNDRYBAG_MAXVOLUME
from .clothes import Clothes, ClothesState

from enum import Enum
from typing import List
from datetime import datetime

class MaximumVolumeExceedError(Exception) :
    pass

class LaundryBagState(Enum) :
    COLLECTING = '수거중'
    READY = '세탁준비'
    RUN = '세탁중'
    DONE = '세탁완료'

class LaundryBag(list):
    def __init__(self, laundrybagid : str, clothes_list: List[Clothes], created_at: datetime):
        super().__init__(clothes_list)  
        ## TODO : if clothes does not have orderid, it cannot be in laundrybag
        self.laundrybagid = laundrybagid
        self.created_at = created_at
        self.status = LaundryBagState.COLLECTING
        self.clothes_list = clothes_list

        # 옷상태를 '세탁분류' 상태로 전환
        for clothes in self.clothes_list :
            clothes.status = ClothesState.DISTRIBUTED

    def can_contain(self, volume : float) :
        return self.volume + volume <= LAUNDRYBAG_MAXVOLUME

    def append(self, clothes) :
        if self.can_contain(clothes.volume) :
            clothes.status = ClothesState.DISTRIBUTED
            self.clothes_list.append(clothes)
        else :
            raise MaximumVolumeExceedError

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