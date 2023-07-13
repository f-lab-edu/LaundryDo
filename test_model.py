import pytest

from uuid import uuid4
from model import Clothes, Order, LaundryLabel, LaundryBag, User

from typing import List

from datetime import datetime

time_now = datetime.now()

def divide_order(order : Order)  -> List[LaundryBag] :
    laundrylabeldict = {}
    for clothes in order :
        if clothes.label in laundrylabeldict : 
            laundrylabeldict[clothes.label].append(clothes)
        else :
            laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict





def test_user_request_new_order(new_user, new_order) :
    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(new_user, new_order ) :

    new_user.request_order(new_order)

    new_user.cancel_order(new_order)

    assert new_user.orderlist == []
    
def test_clothes_in_an_order_has_all_same_order_id(new_order) :

    assert len(set(order.orderid for order in new_order)) == 1


def test_order_sort_by_laundrybags() :
    clothes1 = Clothes(clothesid = str(uuid4())[:4], label = LaundryLabel.WASH, volume = 0.3)
    clothes2 = Clothes(clothesid = str(uuid4())[:4], label = LaundryLabel.DRY, volume = 0.3)
    clothes3 = Clothes(clothesid = str(uuid4())[:4], label = LaundryLabel.DRY, volume = 0.3)
    clothes4 = Clothes(clothesid = str(uuid4())[:4], label = LaundryLabel.WASH, volume = 0.3)
    order = Order('order1', received_at = time_now, clothes_list = [clothes1, clothes2, clothes3, clothes4])

    laundrylabeldict = divide_order(order)

    assert len(laundrylabeldict.keys()) == 2
    


def test_laundrybags_with_same_laundryLabel_combine_into_same_laundbag() :
    pass




def test_laundrybag_has_same_laundrylabel() :
    pass


def test_allocate_laundrybag_into_laundryMachine() :
    pass


def test_fail_to_allocate_laundrybag_into_laundryMachine_if_broken_or_running() :
    pass


