from .spec import LAUNDRYBAG_MAXVOLUME
from .clothes import Clothes, ClothesState

from enum import Enum
from typing import List
from datetime import datetime


class LaundryBagState(Enum) :
    READY = '세탁준비'
    RUN = '세탁중'
    DONE = '세탁완료'

class LaundryBag(list):
    def __init__(self, clothes_list: List[Clothes], created_at: datetime):
        super().__init__(clothes_list)  
        ## TODO : if clothes does not have orderid, it cannot be in laundrybag
        self.created_at = created_at
        self.status = LaundryBagState.READY

        # 옷상태를 '세탁분류' 상태로 전환
        for clothes in self:
            clothes.status = ClothesState.DISTRIBUTED

    def can_contain(self, volume : float) :
        return self.volumeContained + volume <= LAUNDRYBAG_MAXVOLUME


    @property
    def volumeContained(self):
        return sum(clothes.volume for clothes in self)

    def update_clothes_status(self, status: ClothesState):
        [setattr(clothes, "status", status) for clothes in self]

    @property
    def label(self):
        return next((clothes.label for clothes in self), None)

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.created_at < other.created_at
        else:
            raise TypeError(
                f"{type(other)} cannot be compared with {self.__class__} class."
            )