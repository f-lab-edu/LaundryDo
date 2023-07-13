from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from enum import Enum

class OrderState(Enum) :
    SENDING = '이동중'
    PREPARING = '준비중'
    WASHING = '빨래중'
    SHIPPING = '배송중'

class ClothesState(Enum) :
    CANCELLED = '취소'
    PREPARING = '준비중'
    DIVIDED = '세탁분류' # 세탁 라벨에 따라 분류된 상태
    PROCESSING = '세탁중'
    DONE = '세탁완료'

class LaundryLabel(Enum) :
    WASH = '물세탁'
    DRY = '드라이클리닝' 
    HAND = '손세탁'


class MachineState(Enum) :
    READY = '준비'
    RUNNING = '가동중'
    DONE = '세탁완료' # 세탁 완료 후 laundryBag이 reclaim되어야 다시 '준비'상태로 돌아갈 수 있다.                                                                                                                                                                                                                                                                                                                                                                 꺼내야하는 상태
    BROKEN = '고장'

@dataclass(unsafe_hash = True)
class Clothes :
    clothesid : str
    label : LaundryLabel
    volume : float
    status : ClothesState = field(default = ClothesState.PREPARING)


class LaundryBag(dict) : ## TODO : laundryBag 단일 객체가 아닌, 모든 laundrybag을 포함하는 클래스가 필요하다
    def __init__(self, laundrybagid: str) :
        super().__init__(*arg, **kw)
        self.laundrybagid = laundrybagid
        self.assignedMachine = None # laundryMachine
        self.createdTime = None
        self.clothesBag = {}

    def combine(self, clothes : Clothes) :
        if self.laundrylabel not in self.clothesBag :
            self.clothesBag[clothes.laundrylabel] = [clothes]
            if self.createdTime is None :
                self.createdTime = datetime.now() ## 합쳐진 가장 첫 시점 <- 늦게 들어왔더라도, 먼저 들어온 빨래의 대기시간이 길면, 함께 빨리 빨래 큐에 들어갈 수 있다.
        elif self.laundrylabel in self.clothesBag :
            self.clothesBag[clothes.laundrylabel].append(clothes)
        else :
            print('cannot allocate because (1. volume exceeded) or (2. laundrylabels are different)')

    @property
    def volume(self) :
        return sum(clothes.volume for clothes in self.clothesBag)

    @property
    def laundrylabel(self) :
        return next((clothes.label for clothes in self.clothesBag), None)
        


class Order :
    def __init__(self, orderid: str, received_at : datetime, clothesBag : List[Clothes] = [], orderstate: OrderState = OrderState.SENDING) :
        self.orderid = orderid
        self.received_at = received_at
        self.orderstate = orderstate
        self.clothesBag = clothesBag

    # implement if user can cancel by clothes. allow only cancel by Order Unit.
    # @property
    # def clothesBag(self) :
    #     return [clothes for clothes in self.clothesBag if self.orderstate == OrderState.PREPARING]

    def __len__(self) :
        return len(self.clothesBag)

    def sortbyLaundryLabel(self, laundryBag : LaundryBag) :
        for clothes in self.clothesBag :
            laundryBag.combine(clothes)
            clothes.status = ClothesState.DIVIDED



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

    def assign_laundryBag(self, laundryBag : LaundryBag) :
        pass


class User :
    def __init__(self, id: str, address: str, orderlist : List[Order]) :
        self.id = id
        self.address = address
        self.orderlist = orderlist

    def request_order(self, order: Order) :
        order.orderstate = OrderState.PREPARING
        self.orderlist.append(order)

    def cancel_order(self, order: Order) :
        [selected_order] = [submitted_order for submitted_order in self.orderlist if submitted_order.orderid == order.orderid]


        if selected_order and (selected_order.orderstate == OrderState.PREPARING or selected_order.orderstate == OrderState.SENDING) :
            self.orderlist.remove(selected_order)
        else :
            print(f'order id {order.orderid} does not exist.')


    def request_order_history(self) :
        pass







    