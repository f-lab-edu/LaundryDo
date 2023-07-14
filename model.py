from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from enum import Enum

LAUNDRYBAG_MAXVOLUME = LAUNDRYMACHINE_MAXVOLUME = 25

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
    RUNNING = '세탁중'
    DONE = '세탁완료' # 세탁 완료 후 laundryBag이 reclaim되어야 다시 '준비'상태로 돌아갈 수 있다.                                                                                                                                                                                                                                                                                                                                                                 꺼내야하는 상태
    BROKEN = '고장'

class Clothes :
    def __init__(self, 
                id : str,
                label : LaundryLabel,
                volume : float,
                orderid : str = None,
                status : ClothesState = ClothesState.PREPARING,
                received_at : datetime = None
                ) :
        self.id = id
        self.label = label
        self.volume = volume
        self.orderid = orderid
        self.status = status
        self.received_at = received_at
            
    def __lt__(self, other) :
        if isinstance(other, Clothes) :
            return self.received_at < other.received_at
        else :
            raise TypeError(f'{type(other)} cannot be compared with Clothes class.')


class LaundryBag(list) :
    def __init__(self, clothes_list : List[Clothes], label : LaundryLabel, createdTime: datetime) :
        super().__init__(clothes_list)
        self.createdTime = createdTime
        self.label = label
        self.maxVolume = maxVolume

        # 옷상태를 '세탁분류' 상태로 전환
        for clothes in self :
            clothes.status = ClothesState.DIVIDED


    @property
    def volumeContained(self) :
        return sum(clothes.volume for clothes in self)

    @property
    def label(self) :
        return next((clothes.label for clothes in self), None)



# class LaundryBag(dict) : ## TODO : laundryBag 단일 객체가 아닌, 모든 laundrybag을 포함하는 클래스가 필요하다
#     def __init__(self, laundrybagid: str) :
#         super().__init__(*arg, **kw)
#         self.laundrybagid = laundrybagid
#         self.assignedMachine = None # laundryMachine
#         self.createdTime = None
#         self.clothesBag = {}

#     def combine(self, clothes : Clothes) :
#         if self.laundrylabel not in self.clothesBag :
#             self.clothesBag[clothes.laundrylabel] = [clothes]
#             if self.createdTime is None :
#                 self.createdTime = datetime.now() ## 합쳐진 가장 첫 시점 <- 늦게 들어왔더라도, 먼저 들어온 빨래의 대기시간이 길면, 함께 빨리 빨래 큐에 들어갈 수 있다.
#         elif self.laundrylabel in self.clothesBag :
#             self.clothesBag[clothes.laundrylabel].append(clothes)
#         else :
#             print('cannot allocate because (1. volume exceeded) or (2. laundrylabels are different)')

#     @property
#     def volume(self) :
#         return sum(clothes.volume for clothes in self.clothesBag)

#     @property
#     def laundrylabel(self) :
#         return next((clothes.label for clothes in self.clothesBag), None)
        

class Order(list) :
    def __init__(self, 
                 orderid: str, 
                 clothes_list : List[Clothes],
                 received_at : datetime, 
                 orderstate: OrderState = OrderState.SENDING):
        super().__init__(clothes_list)
        self.orderid = orderid
        self.received_at = received_at
        self.orderstate = orderstate

        for clothes in self :
            clothes.orderid = self.orderid
            clothes.received_at = self.received_at

        def pop(self, index) :
            # self[index].orderid = None # TODO : Not working
            return super().pop(index)

        def remove(self, item) :
            item.orderid = None
            super().remove(item)

        def __setitem__(self, index, item):
            # super().__setitem__(index, item)
            raise NotImplementedError

        def insert(self, index, item):
            # super().insert(index, item)
            raise NotImplementedError

        def append(self, item):
            # super().append(item)
            raise NotImplementedError

        def extend(self, other):
            # if isinstance(other, type(self)):
            #     super().extend(other)
            # else:
            #     super().extend(item for item in other)
            raise NotImplementedError

        @property
        def volume(self) :
            return sum(clothes.volume for clothes in self)




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

    # def assign_laundryBag(self, laundryBag : LaundryBag) :
    #     pass


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







    