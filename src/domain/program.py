from .spec import LAUNDRYBAG_MAXVOLUME, LAUNDRY_MINVOLUME
from .clothes import Clothes, ClothesState, LaundryLabel
from .order import Order, OrderState
from .laundrybag import LaundryBag, LaundryBagState

from .repository import OrderRepository, LaundryBagRepository

from typing import List, Dict
from datetime import datetime


def request_order(order_repository : OrderRepository, order : Order) :
    OrderRepository.add(Order)

def cancel_order(order_repository : OrderRepository, orderid : str) :

    [order] = OrderRepository.get(orderid)
    if order.status in [OrderState.SENDING, OrderState.PREPARING] :
        # cancel the order
        raise NotImplementedError
    


def distribute_order(order_repository : OrderRepository) -> Dict[LaundryLabel, LaundryBag]:
    laundrylabeldict = {}

    order_list = order_repository.get_by_status(status = OrderState.SENDING)

    for order in order_list:
        for clothes in order.clothes_list:
            if clothes.label in laundrylabeldict:
                laundrylabeldict[clothes.label].append(clothes)
            else:
                laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict




def put_in_laundrybag(laundrybag_repository : LaundryBagRepository, laundryBagDict : Dict[LaundryLabel, List[Clothes]]) :

    # TODO : 수정 필요. 현재 새로운 laundrybag 이름 생성시, 전체 laundrybag 갯수에서 +1'
    laundrybag_num = len(laundrybag_repository.list())

    for laundrylabel, clothes_list in laundryBagDict.items():
        # sort by date
        clothes_list.sort()

        # 대기 중인 Laundrybag은 항상 한 개 라고 가정.
        target_bag = laundrybag_repository.get_waitingbag_by_label(label = laundrylabel)

        if not target_bag :
            target_bag = LaundryBag(laundrybagid = f'test-laundrybag-{laundrybag_num}', clothes_list=[], created_at = datetime.now() ) ## TODO : naming of the laundrybagid
            

        for clothes in clothes_list :
            if target_bag.can_contain(clothes.volume) :
                target_bag.append(clothes)
            else :
                if target_bag.volume >= LAUNDRY_MINVOLUME :
                    target_bag.status = LaundryBagState.READY
                    ### add to the repository
                    laundrybag_repository.add(target_bag)

                    target_bag = LaundryBag(laundrybagid = f'test-laundrybag-{laundrybag_num}', clothes_list=[clothes], created_at = datetime.now() ) ## TODO : naming of the laundrybagid
                else :
                    raise ValueError('if minvolume is not fulfilled, try other clothes?')
    
        laundrybag_repository.add(target_bag)

    
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
        for clothes in laundryBag.clothes_list:
            clothes.status = ClothesState.RECLAIMED
            if clothes.orderid not in reclaimed_dict:
                reclaimed_dict[clothes.orderid] = [clothes]
            else:
                reclaimed_dict[clothes.orderid].append(clothes)

    reclaimed_list = []
    for orderid, reclaimed in reclaimed_dict.items():
        reclaimed_list.append(
            Order(orderid=orderid, clothes_list=reclaimed, status=OrderState.RECLAIMING)
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