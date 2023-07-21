from .clothes import Clothes

from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import datetime


class OrderState(Enum) :
    CANCELLED = '취소'
    SENDING = '이동중'
    PREPARING = '준비중'
    WASHING = '세탁중'
    RECLAIMING = '정리중'
    SHIP_READY = '배송준비완료'
    SHIPPING = '배송중'
    DONE = '완료'

class Order:
    def __init__(
        self,
        orderid: str,
        clothes_list: List[Clothes] = [],
        received_at: datetime | None = None,  ## TODO : received time by each status?
        status: OrderState = OrderState.SENDING, ## TODO : private property
    ):
        # super().__init__(clothes_list)
        self.clothes_list = clothes_list
        self.orderid = orderid
        self.received_at = received_at
        self.status = status

        for clothes in self.clothes_list :
            clothes.orderid = self.orderid
            # clothes.received_at = self.received_at

        # def pop(self, index):
        #     # self[index].id = None # TODO : Not working
        #     return super().pop(index)

        # def remove(self, item):
        #     item.orderid = None
        #     super().remove(item)

        # def __setitem__(self, index, item):
        #     # super().__setitem__(index, item)
        #     raise NotImplementedError

        # def insert(self, index, item):
        #     # super().insert(index, item)
        #     raise NotImplementedError

        # def append(self, item):
        #     # super().append(item)
        #     raise NotImplementedError

        # def extend(self, other):
        #     # if isinstance(other, type(self)):
        #     #     super().extend(other)
        #     # else:
        #     #     super().extend(item for item in other)
        #     raise NotImplementedError

        @property
        def volume(self) -> float :
            return sum(clothes.volume for clothes in self.clothes_list )