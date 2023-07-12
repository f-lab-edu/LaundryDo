from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

class OrderState(Enum) :
    PREPARING = '준비중'
    SENDING = '이동중'
    WASHING = '빨래중'
    SHIPPING = '배송중'


class LaundryLabel(Enum) :
    WASH = '물세탁'
    DRY = '드라이클리닝' 
    HAND = '손세탁'


class MachineState(Enum) :
    READY = '준비'
    RUNNING = '가동중'
    BROKEN = '고장'


@dataclass(unsafe_hash = True)
class Clothes :
    clothesid : str
    label : LaundryLabel
    volume : float


@dataclass(unsafe_hash = True)
class Order :
    orderid : str
    received_at : datetime
    orderstate : OrderState = field(default = OrderState.PREPARING)
    clothesbag : List[Clothes] = field(default_factory = list)




class LaundryBag :
    def __init__(self, laundrybagid: str, clothesBag : List[Clothes], volume : float) :
        self.laundrybagid = laundrybagid
        self.clothesBag = clothesBag
        self.assignedMachine = None # laundryMachine

    def allocate(self, clothes : Clothes) :
        if clothes.label == self.laundrylabel or self.laundrylabel is None :
            self.clothesBag.append(clothes)

    @property
    def volume(self) :
        return sum(clothes.volume for clothes in self.clothesBag)

    @property
    def laundrylabel(self) :
        return next((clothes.label for clothes in self.clothesBag), None)
        


class LaundryMachine :
    def __init__(self, laundrymachineid: str, startTime : datetime, estimatedEndTime : datetime, maxVolume : float ) :
        self.laundrymachineid = laundrymachineid
        self.startTime = startTime
        self.estimatedEndTime = estimatedEndTime
        self.maxVolume = maxVolume
        self.containedBags = [] # List[LaundryBag]

    @property
    def volumeContained(self) :
        return sum(bag.volume for bag in self.containedBags)



class User :
    def __init__(self, id: str, address: str, orderlist : List[Order]) :
        self.id = id
        self.address = address
        self.orderlist = orderlist

    def request_order(self, order: Order) :
        self.orderlist.append(order)

    def request_order_history(self) :
        pass







    