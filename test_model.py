import pytest
from model import Clothes, Order, LaundryLabel, User
from datetime import datetime

time_now = datetime(2023, 7, 12, 20, 48, 13)

def place_order() :
    clothes1 = Clothes('blue top', LaundryLabel.DRY, 0.2)
    clothes2 = Clothes('black jeans', LaundryLabel.WASH, 0.3)
    order = Order('order1', received_at = time_now, clothesbag = [clothes1, clothes2])

    return order


def test_user_request_new_order() :
    user1 = User(id = 'eunsung', address = '서울시 송파구', orderlist = [])
    
    order1 = place_order()
    
    user1.request_order(order1)

    assert user1.orderlist == [order1]


def test_user_cancel_order() :
    pass



def test_orders_allocate_into_laundrybags() :
    pass


def test_laundrybag_has_same_laundrylabel() :
    pass


def test_allocate_laundrybag_into_laundryMachine() :
    pass


def test_fail_to_allocate_laundrybag_into_laundryMachine_if_broken_or_running() :
    pass


