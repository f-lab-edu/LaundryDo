from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from enum import Enum

LAUNDRYBAG_MAXVOLUME = LAUNDRYMACHINE_MAXVOLUME = 25

class OrderState(Enum) :
    SENDING = '이동중'
    PREPARING = '준비중'
    WASHING = '빨래중'
    RECLAIMING = '정리중'
    SHIP_READY = '배송준비완료'
    SHIPPING = '배송중'

class ClothesState(Enum) :
    CANCELLED = '취소'
    PREPARING = '준비중'
    DIVIDED = '세탁전분류' # 세탁 라벨에 따라 분류된 상태
    PROCESSING = '세탁중'
    STOPPED = '일시정지' # 세탁기 고장이나 외부 요인으로 세탁 일시 중지
    DONE = '세탁완료'
    RECLAIMED = '세탁후분류'

class LaundryLabel(Enum) :
    WASH = '물세탁'
    DRY = '드라이클리닝' 
    HAND = '손세탁'


class MachineState(Enum) :
    READY = '준비'
    STOP = '정지'
    RUNNING = '세탁중'
    DONE = '세탁완료' # 세탁 완료 후 laundryBag이 reclaim되어야 다시 '준비'상태로 돌아갈 수 있다.                                                                                                                                                                                                                                                                                                                                                                 꺼내야하는 상태
    BROKEN = '고장'


def time_required_for_volume(time, volume) : 
    if 0 < volume <= 10 :
        time *= 1
    elif 10 < volume < 20 :
        time *= 1.5
    elif 20 <= volume < 25 :
        time *= 2
    else :
        raise ValueError(f'{volume} is not valid unit.')
    return int(time )

LaundryTimeTable = {
    LaundryLabel.WASH :  60,
    LaundryLabel.DRY :  80,
    LaundryLabel.HAND : 100
}



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
        if other.__class__ is self.__class__ :
            return self.received_at < other.received_at
        else :
            raise TypeError(f'{type(other)} cannot be compared with Clothes class.')

class Order(list) :
    def __init__(self, 
                 id: str, 
                 clothes_list : List[Clothes],
                 received_at : datetime = None, ## TODO : received time by each status? 
                 status: OrderState = OrderState.SENDING):
        super().__init__(clothes_list)
        self.id = id
        self.received_at = received_at
        self.status = status

        for clothes in self :
            clothes.orderid = self.id
            clothes.received_at = self.received_at

        def pop(self, index) :
            # self[index].id = None # TODO : Not working
            return super().pop(index)

        def remove(self, item) :
            item.id = None
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



class LaundryBag(list) :
    def __init__(self, clothes_list : List[Clothes], createdTime: datetime) :
        super().__init__(clothes_list) ## TODO : if clothes does not have orderid, it cannot be in laundrybag
        self.createdTime = createdTime

        # 옷상태를 '세탁분류' 상태로 전환
        for clothes in self :
            clothes.status = ClothesState.DIVIDED


    @property
    def volumeContained(self) :
        return sum(clothes.volume for clothes in self)

    def update_clothes_status(self, status: ClothesState) :
        [setattr(clothes, 'status', status) for clothes in self]

    @property
    def label(self) :
        return next((clothes.label for clothes in self), None)

    def __lt__(self, other) :
        if other.__class__ is self.__class__ :
            return self.createdTime < other.createdTime
        else :
            raise TypeError(f'{type(other)} cannot be compared with {self.__class__} class.')






class LaundryMachine :
    def __init__(self, id: str) :
        self.id = id
        self.contained = None # LaundryBag
        
        self.startTime = None
        self.lastupdateTime = None
        self.runtime = timedelta(minutes = 0)
        
        self.status = MachineState.READY

    @property
    def volumeContained(self) :
        if self.contained is None : return None
        return self.contained.volumeContained

    @property
    def label(self) :
        if self.contained is None : return None
        return self.contained.label

    @property
    def requiredTime(self) :
        if self.label is None : 
            return None
        return time_required_for_volume(LaundryTimeTable[self.label], self.volumeContained)

    def get_runtime(self, exec_time : datetime) :

        if self.lastupdateTime and self.status == MachineState.RUNNING :
            return self.runtime + (exec_time - self.lastupdateTime)
        else :
            return self.runtime
            


    def remainingTime(self, exec_time: datetime) :
        return timedelta(minutes = self.requiredTime) - self.get_runtime(exec_time)
                    

    def can_contain(self, laundryBag : LaundryBag) :
        return laundryBag.volumeContained <= LAUNDRYMACHINE_MAXVOLUME 


    def putLaundryBag(self, laundrybag : LaundryBag) :
        if self.can_contain(laundrybag) and self.status not in [MachineState.RUNNING, MachineState.BROKEN]: 
            self.contained = laundrybag
        else :
            raise ValueError('cannot contain the bag, too large.')


    def start(self, exec_time: datetime) :
        if self.status == MachineState.RUNNING :
            raise ValueError('machine is already running')
        elif self.status == MachineState.BROKEN :
            raise ValueError('machine is broken.')

        if self.contained is None :
            raise ValueError('No LaundryBag in the Machine')

        self.startTime = exec_time
        self.lastupdateTime = self.startTime
        self.status = MachineState.RUNNING


    def resume(self, exec_time: datetime) : 
        if self.status == MachineState.STOP : 
            self.lastupdateTime = exec_time
            self.status = MachineState.RUNNING
        else :
            raise ValueError(f'cannot resume when {self.status}')


    def stop(self, exec_time: datetime) :
        if self.status == MachineState.RUNNING :
            self.status = MachineState.STOP
            # now = datetime.now()
            self.runtime += exec_time - self.lastupdateTime
            self.lastupdateTime = exec_time
        else :
            raise ValueError(f'cannot stop when {self.status}')


class User :
    def __init__(self, id: str, address: str, orderlist : List[Order]) :
        self.id = id
        self.address = address
        self.orderlist = orderlist

    def request_order(self, order: Order) :
        order.status = OrderState.PREPARING
        self.orderlist.append(order)

    def cancel_order(self, order: Order) :
        [selected_order] = [submitted_order for submitted_order in self.orderlist if submitted_order.id == order.id]


        if selected_order and (selected_order.status == OrderState.PREPARING or selected_order.status == OrderState.SENDING) :
            self.orderlist.remove(selected_order)
        else :
            print(f'order id {order.id} does not exist.')


    def request_order_history(self) :
        pass







    