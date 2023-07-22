import pytest
from src.domain import (
    LaundryLabel, 
    ClothesState, 
    LaundryBag, 
    distribute_order, 
    put_in_laundrybag, 
    get_clothes_in_process,
    reclaim_clothes_into_order
)

from src.infrastructure.db.memory.repository import MemoryLaundryBagRepository, MemoryOrderRepository
from src.infrastructure.db.sqlalchemy.repository import SqlAlchemyLaundryBagRepository, SqlAlchemyOrderRepository


from datetime import datetime

today = datetime.today()

def test_clothes_in_an_order_has_all_same_order_id(order_factory, clothes_factory):

    new_order = order_factory(clothes_list = [clothes_factory() for _ in range(10)])
    assert len(set(order.orderid for order in new_order.clothes_list)) == 1


def test_order_sort_by_laundrybags(order_factory, clothes_factory):
    clothes1 = clothes_factory(label=LaundryLabel.WASH, volume=0.01)
    clothes2 = clothes_factory(label=LaundryLabel.DRY, volume=0.01)
    clothes3 = clothes_factory(label=LaundryLabel.DRY, volume=0.01)
    clothes4 = clothes_factory(label=LaundryLabel.WASH, volume=0.01)
    order = order_factory(
        received_at=today,
        clothes_list=[clothes1, clothes2, clothes3, clothes4],
    )
    order_repo = MemoryOrderRepository(orders = [order])

    laundrylabeldict = distribute_order(order_repo)

    assert len(laundrylabeldict) == 2


def test_multiple_orders_distributed_into_laundrybags(session, order_factory, clothes_factory):
    multiple_orders = []
    label_options = [LaundryLabel.WASH, LaundryLabel.HAND]
    
    order_repo = SqlAlchemyOrderRepository(session)
    
    for i in range(10) :
        clothes_list = [clothes_factory(label = label_options[ i%2 ], volume = 1, received_at = today) for _ in range(5)]
        new_order = order_factory(clothes_list = clothes_list )
        multiple_orders.append(new_order)
        order_repo.add(new_order)
    # load order, laundrybag repository
    
    
    laundrybag_repo = SqlAlchemyLaundryBagRepository(session)


    laundrybag_dict = distribute_order(order_repo)
    put_in_laundrybag(laundrybag_repo, laundrybag_dict)

    assert len(laundrybag_repo.list()) == 2 and len(multiple_orders) == 10


def test_multiple_orders_with_same_label_and_over_max_volume_distributed_into_laundrybags(order_factory, clothes_factory) :
    pass





#################
# reclaim order #
#################

def test_clothes_finished_laundry_reclaim_by_orderid(clothes_factory):
    orderid_list = ["EUNSUNG_o3_230715", "SAM_o18_230714", "LUKE_01_230716"]

    freshly_done_laundrybags = []

    for i in range(len(orderid_list)):
        orderid = orderid_list[i]
        clothes_list = [clothes_factory(volume = 1) for _ in range(5)]
        for clothes in clothes_list:  # assign orderid to clothes
            clothes.orderid = orderid

        laundryBag = LaundryBag(laundrybagid = 'test-laundrybag', clothes_list = clothes_list, created_at=None)

        ## TODO : better way to simulate to update laundry process DONE
        for clothes in laundryBag:
            clothes.status = ClothesState.DONE
        freshly_done_laundrybags.append(laundryBag)

    reclaimed_order_list = reclaim_clothes_into_order(freshly_done_laundrybags)

    assert set([order.orderid for order in reclaimed_order_list]) == set(orderid_list) and \
                len(reclaimed_order_list) == len(orderid_list)


def test_check_every_clothes_by_orderid_reclaimed():
    pass