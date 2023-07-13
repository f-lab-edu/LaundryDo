import pytest
from model import Clothes, Order, LaundryLabel, User
from datetime import datetime



def test_user_request_new_order(new_user, new_order) :
    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(new_user, new_order ) :

    new_user.request_order(new_order)

    new_user.cancel_order(new_order)

    assert new_user.orderlist == []
    


def test_order_sort_by_laundrybags(new_order) :
    # new_order.sortbyLaundryLabel()
    pass
    


def test_laundrybags_with_same_laundryLabel_combine_into_same_laundbag() :
    pass




def test_laundrybag_has_same_laundrylabel() :
    pass


def test_allocate_laundrybag_into_laundryMachine() :
    pass


def test_fail_to_allocate_laundrybag_into_laundryMachine_if_broken_or_running() :
    pass


