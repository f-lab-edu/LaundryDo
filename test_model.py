import pytest

from uuid import uuid4
from model import Clothes, Order, LaundryLabel, LaundryBag, User

from typing import List, Dict

from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)


# clothes, order, laundrybag, user

def divide_order(order : Order)  -> List[LaundryBag] :
    laundrylabeldict = {}
    for clothes in order :
        if clothes.label in laundrylabeldict : 
            laundrylabeldict[clothes.label].append(clothes)
        else :
            laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict

def put_in_laundrybag(laundryBagDict : Dict[LaundryLabel, List[Clothes]]) :

    for laundrylabel, clothes_list in laundryBagDict.items() :
        LaundryBag(clothes_list = clothes_list, label = laundrylabel, createdTime = datetime.now())
    


###########
# Clothes #
###########


def test_sort_clothes_by_time() :
    clothes_today = Clothes(id= 'green top', volume = 0.3, label = LaundryLabel.WASH, received_at = today)
    clothes_yesterday = Clothes(id= 'blue jean', volume = 0.4, label = LaundryLabel.WASH, received_at = yesterday)
    clothes_longtimeago = Clothes(id= 'yellow skirt', volume = 0.7, label = LaundryLabel.WASH, received_at = longtimeago)

    assert sorted([clothes_yesterday, clothes_longtimeago, clothes_today]) == [clothes_longtimeago, clothes_yesterday, clothes_today]



#############
#    User   #
#############
def test_user_request_new_order(new_user, new_order) :
    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(new_user, new_order ) :

    new_user.request_order(new_order)

    new_user.cancel_order(new_order)

    assert new_user.orderlist == []


#############
#   Order   #
#############
def test_clothes_in_an_order_has_all_same_order_id(new_order) :

    assert len(set(order.orderid for order in new_order)) == 1


def test_order_sort_by_laundrybags() :
    clothes1 = Clothes(id = str(uuid4())[:4], label = LaundryLabel.WASH, volume = 0.3)
    clothes2 = Clothes(id = str(uuid4())[:4], label = LaundryLabel.DRY, volume = 0.3)
    clothes3 = Clothes(id = str(uuid4())[:4], label = LaundryLabel.DRY, volume = 0.3)
    clothes4 = Clothes(id = str(uuid4())[:4], label = LaundryLabel.WASH, volume = 0.3)
    order = Order('order1', received_at = today, clothes_list = [clothes1, clothes2, clothes3, clothes4])

    laundrylabeldict = divide_order(order)

    assert len(laundrylabeldict) == 2

def test_multiple_orders_divided_into_laundrybags(new_order) :    
    multiple_orders = [new_order for _ in range(10)]




##############
# LaundryBag #
##############


def test_laundrybag_clothes_status_changed_to_divided(new_order) :
    orders = new_order


def test_laundrybags_with_same_laundryLabel_combine_into_same_laundbag() :
    pass




def test_laundrybag_has_same_laundrylabel() :
    pass


def test_allocate_laundrybag_into_laundryMachine() :
    pass


def test_fail_to_allocate_laundrybag_into_laundryMachine_if_broken_or_running() :
    pass


