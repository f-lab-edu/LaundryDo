from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, timedelta

from src.domain import (
    ClothesState,
    LaundryBagState,
    OrderState,
    LaundryLabel,
    MachineState
)



class Clothes(BaseModel):
    model_config = ConfigDict(from_attributes = True, use_enum_values = True)
    clothesid : str
    label: LaundryLabel = LaundryLabel.UNDEFINED
    volume: float


    # orderid: Optional[str] = None
    # laundrybagid : Optional[str] = None
    # status: ClothesState = ClothesState.PREPARING
    # received_at: Optional[datetime] = None
    # model_config = {
    #     "json_schema_extra" : {
    #         "examples" : [
    #             {
    #                 "clothesid" : "흰 티셔츠",
    #                 "description" : "세탁 대상 옷 예시",
    #                 "label" : LaundryLabel.DRY,
    #                 "volume" : 3,
    #             }
    #         ]
    #     }
    # }


class Order(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    orderid : str
    userid : int
    clothes_list : List[Clothes] = []
    received_at : Optional[datetime] = None
    status : OrderState = OrderState.SENDING

class OrderCreate(BaseModel) :
    model_config = ConfigDict(from_attributes = True)
    # userid : str
    clothes_list : List[Clothes] | None
    # received_at : datetime | None

    


class User(BaseModel) :
    model_config = ConfigDict(from_attributes = True)
    userid : str
    address : str
    orderlist : List[Order] | None = []


# class UserCreate(User) :
#     password : str
    

class LaundryBag(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    laundrybagid : str
    created_at : Optional[datetime] = None
    status : LaundryBagState = LaundryBagState.COLLECTING
    clothes_list : List[Clothes]
    volume : float

    # def __init__(self, **kwargs) :
    #     super().__init__(**kwargs)
    #     # 옷상태를 '세탁분류' 상태로 전환
    #     for clothes in kwargs['clothes_list'] :
    #         clothes.status = ClothesState.DISTRIBUTED

class Machine(BaseModel) :
    model_config = ConfigDict(from_attributes = True)

    machineid : str
    contained : List[LaundryBag]
    started_at : Optional[datetime]
    updated_at : Optional[datetime]
    runtime : Optional[timedelta]
    status : MachineState
    volume : float
