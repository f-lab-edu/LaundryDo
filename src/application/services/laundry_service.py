from concurrent.futures import wait
from select import select
from typing import List, Dict
from src.domain import Clothes, LaundryBag, LaundryLabel, LaundryBagState, Order, OrderState, ClothesState
from src.domain.spec import LAUNDRYBAG_MAXVOLUME, MACHINE_MAXVOLUME

from src.domain.repository import UserRepository, OrderRepository, LaundryBagRepository, MachineRepository
from datetime import datetime

from src.domain.services import distribute_order, put_in_laundrybag#, check_clothes_in_order_is_fully_reclaimed, reclaim_clothes_into_order


class LaundryService :

    def __init__(self, 
                session,
                order_repository,
                clothes_repository,
                laundrybag_repository,
                machine_repository,
                ): 

        self.order_repository = order_repository(session)
        self.clothes_repository = clothes_repository(session)
        self.laundrybag_repository = laundrybag_repository(session)
        self.machine_repository = machine_repository(session)

    def run_process(self, order : Order) :

        self.order_repository.add(order)

        laundrylabeldict = distribute_order([order])
        laundryBagList = put_in_laundrybag(laundrylabeldict)

        machines = self.machine_repository.list()

        # get available machine
        for laundrybag in laundryBagList :
            allocate(machines, laundrybag)

        # load laundrybag repo again
        laundrybags_to_be_reclaimed = self.laundrybag_repository.all()
        reclaimed_list = reclaim_clothes_into_order(laundrybags_to_be_reclaimed)

        # load order repo again to check order has benn fully reclaimed
        orders = self.order_repository.list()

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
        order.status = OrderState.SHIPPING

