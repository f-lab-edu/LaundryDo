from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRY_MINVOLUME
from src.domain.clothes import Clothes, ClothesState, LaundryLabel
from src.domain.order import Order, OrderState
from src.domain.laundrybag import LaundryBag, LaundryBagState
from src.domain.machine import Machine, MachineState
from src.domain.repository import OrderRepository, LaundryBagRepository, MachineRepository
from src.application.unit_of_work import AbstractUnitOfWork

from typing import List, Dict
from datetime import datetime


class OrderNotFoundError(Exception) :
    pass


def request_order(uow : AbstractUnitOfWork, orderid, clothes_list, received_at, status) :
    with uow :
        uow.orders.add(Order(orderid, [Clothes(**dict(clothes)) for clothes in clothes_list], received_at, status))
        uow.commit()


def cancel_order(uow : AbstractUnitOfWork, userid : str, orderid : str) :
    with uow : 
        [order] = uow.orders.filter(userid = userid).get(orderid)
        if order.status in [OrderState.SENDING, OrderState.PREPARING] :
            # cancel the order
            raise OrderNotFoundError
        uow.commit()
    return order


# order -> laundrybags process
# get waiting laundrybags
# sort order.clothes_list by label
# put in laundrybag if laundrybag can contain the clothes, else make new laundrybag


def distribute_order(order_list : List[Order]) -> Dict[LaundryLabel, List[Clothes]]:
    laundrylabeldict = {}

    for order in order_list:
        for clothes in order.clothes_list:
            if clothes.label in laundrylabeldict:
                laundrylabeldict[clothes.label].append(clothes)
            else:
                laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict


def put_clothes_in_laundrybag(laundrybag : LaundryBag, clothes : Clothes) -> LaundryBag:
    if laundrybag.can_contain(clothes.volume) :
        laundrybag.append(clothes)
    else :
        # 더 이상 clothes를 담지 못한다면, 세탁기로 이동하기 위한 상태로 변경
        laundrybag.status = LaundryBagState.READY
        laundrybag = LaundryBag(
                        laundrybagid = f'bag-{clothes.label}-{int(laundrybag.laundrybagid.split("-")[-1]) + 1}',
                        clothes_list = [clothes],
                                )
    return laundrybag

    
def allocate_laundrybag(uow : AbstractUnitOfWork) :
    with uow :
        laundrylabeldict = distribute_order(uow.orders)

        for laundrylabel, clothes_list in laundrylabeldict.items() :
            waiting_bag = uow.laundrybags.get_waitingbag_by_label(label = laundrylabel)
            if not waiting_bag :
                waiting_bag = LaundryBag(laundrybagid = f'bag-{laundrylabel}-0')

            for clothes in clothes_list :
                waiting_bag = put_clothes_in_laundrybag(waiting_bag, clothes)
        uow.commit()


def reclaim_clothes_into_order(finished_laundrybags : List[LaundryBag]) -> List[Order]:
    
    reclaimed_dict = {}

    for laundryBag in finished_laundrybags:
        for clothes in laundryBag.clothes_list:
            clothes.status = ClothesState.RECLAIMED
            if clothes.orderid not in reclaimed_dict:
                reclaimed_dict[clothes.orderid] = [clothes]
            else:
                reclaimed_dict[clothes.orderid].append(clothes)

    return reclaimed_dict


def get_clothes_in_process(order: Order) -> List[Clothes]:
    '''
    Before shipping, check which clothes is not yet reclaimed.
    '''
    clothes_in_process = []

    for clothes in order.clothes_list:
        if clothes.status != ClothesState.RECLAIMED:
            clothes_in_process.append(clothes)
    return clothes_in_process


def allocate(uow : AbstractUnitOfWork, laundrybag : LaundryBag) :

    with uow :
        available_machines = uow.machines.get_by_status(status = MachineState.READY)
        
        try :
            machine = next(available_machines)

            machine.put(laundrybag)
            uow.commit()
        except StopIteration :
            print('No available Machine right now. Putting laundrybag in waiting list')    
            # TODO : [LaundryBag -> Machine]
            # how to monitor laundrybag that was not able to be allocated at once.

def ship(uow : AbstractUnitOfWork, order: Order) : 
    if get_clothes_in_process(order) is None and order.status == OrderState.SHIP_READY :
        
        with uow :
            order.status = OrderState.SHIPPING
            uow.commit()