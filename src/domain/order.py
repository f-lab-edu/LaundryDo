from .clothes import Clothes

from pydantic import BaseModel, ConfigDict, validator
from enum import Enum
from typing import List, Optional
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

class Order(BaseModel):
    ## TODO : received time by each status?
    ## TODO : private property
    model_config = ConfigDict(from_attributes = True, extra = 'allow')

    orderid : str
    clothes_list : List[Clothes] = []
    received_at : Optional[datetime] = None
    status : OrderState = OrderState.SENDING
    
    def __init__(self, **kwargs) :
        super().__init__(**kwargs)
        for clothes in kwargs['clothes_list'] :
            clothes.orderid = kwargs['orderid']

    @property
    def volume(self) -> float :
        return sum(clothes.volume for clothes in self.clothes_list)