from .spec import LAUNDRYBAG_MAXVOLUME
from .clothes import Clothes, ClothesState, LaundryLabel
from .order import Order, OrderState
from .laundrybag import LaundryBag

from typing import List, Dict
from datetime import datetime

def distribute_order(order_list: List[Order]) -> List[LaundryBag]:
    laundrylabeldict = {}

    for order in order_list:
        for clothes in order:
            if clothes.label in laundrylabeldict:
                laundrylabeldict[clothes.label].append(clothes)
            else:
                laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict



def put_in_laundrybag(laundryBagDict : Dict[LaundryLabel, List[Clothes]]) :

    laundryBagList = []
    for laundrylabel, clothes_list in laundryBagDict.items():
        # sort by date
        clothes_list.sort()

        # split clothes_list by max volume
        laundryBag = LaundryBag(clothes_list=[], createdTime=datetime.now())

        while clothes_list:
            clothes = clothes_list.pop()
            if clothes.volume + laundryBag.volumeContained <= LAUNDRYBAG_MAXVOLUME:
                laundryBag.append(clothes)
            else:
                laundryBagList.append(laundryBag)
                laundryBag = LaundryBag(
                    clothes_list=[clothes], createdTime=datetime.now()
                )

    return laundryBagList

    
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


def get_clothes_in_process(order: Order) -> List[Clothes]:
    '''
    Before shipping, check which clothes is not yet reclaimed.
    '''
    clothes_in_process = []

    for clothes in order:
        if clothes.status != ClothesState.RECLAIMED:
            clothes_in_process.append(clothes)
    return clothes_in_process