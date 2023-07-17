from concurrent.futures import wait
from select import select
from typing import List, Dict
from model import Clothes, LaundryBag, LaundryLabel, BagState, LAUNDRYBAG_MAXVOLUME, LAUNDRYMACHINE_MAXVOLUME, Order, OrderState
from repository import UserRepository, OrderRepository, LaundryBagRepository, MachineRepository
from datetime import datetime

from test_model import check_clothes_in_order_is_fully_reclaimed, distribute_order, reclaim_clothes_into_order


class LaundryService :

    def __init__(self, 
                order_repository,
                clothes_repository,
                laundrybag_repository,
                laundrymachine_repository,
                ): 

    def run_process(self, orderid : str) :

        order = order_repository.get(orderid)

        laundrylabeldict = distribute_order([order])
        laundryBagList = put_in_laundrybag(laundrylabeldict)

        machines = laundrymachine_repository.all()

        # get available machine
        for laundrybag in laundryBagList :
            allocate(machines, laundrybag)

        # load laundrybag repo again
        laundrybags_to_be_reclaimed = laundrybag_repository.all()
        reclaimed_list = reclaim_clothes_into_order(laundrybags_to_be_reclaimed)

        # load order repo again to check order has benn fully reclaimed
        orders = order_repository.all()

        for order in orders :
            if check_clothes_in_order_is_fully_reclaimed(order) :
                ship(order)

        


def reclaim_clothes_into_order(laundryBag_list: List[LaundryBag]) -> List[Order]:
    assert all(
        [
            clothes.status == ClothesState.DONE
            for laundryBag in laundryBag_list
            for clothes in laundryBag
        ]
    )

    reclaimed_dict = {}

    for laundryBag in laundryBag_list:
        for clothes in laundryBag:
            clothes.status = ClothesState.RECLAIMED
            if clothes.orderid not in reclaimed_dict:
                reclaimed_dict[clothes.orderid] = [clothes]
            else:
                reclaimed_dict[clothes.orderid].append(clothes)

    reclaimed_list = []
    for orderid, reclaimed in reclaimed_dict.items():
        reclaimed_list.append(
            Order(id=orderid, clothes_list=reclaimed, status=OrderState.RECLAIMING)
        )

    return reclaimed_list


def check_clothes_in_order_is_fully_reclaimed(order: Order):
    for clothes in order:
        if clothes.status != ClothesState.RECLAIMED:
            return False
    return True


def ship(order: Order):
    if check_clothes_in_order_is_fully_reclaimed(order):
        order.status = OrderState.SHIP_READY

