from src.domain import LaundryLabel, LaundryBagState, LaundryBag, ClothesState, OrderState
from src.application import (
    request_order,
    cancel_order,
    distribute_order,
    put_clothes_in_laundrybag,
    reclaim_clothes_into_order,
    get_clothes_in_process,
    allocate_laundrybag, 
    ship
)

from src.infrastructure.repository import FakeSession

from src.application.unit_of_work import SqlAlchemyUnitOfWork, MemoryUnitOfWork

from src.infrastructure.repository import MemoryOrderRepository, MemoryLaundryBagRepository
from src.infrastructure.repository import SqlAlchemyOrderRepository, SqlAlchemyLaundryBagRepository

import pytest
from datetime import datetime
from uuid import uuid4

today = datetime.today()





def test_order_sort_by_laundrybags(order_factory, clothes_factory):
    
    session = FakeSession()
    order_repo = MemoryOrderRepository(session)

    clothes1 = clothes_factory(label=LaundryLabel.WASH, volume=0.01)
    clothes2 = clothes_factory(label=LaundryLabel.DRY, volume=0.01)
    clothes3 = clothes_factory(label=LaundryLabel.DRY, volume=0.01)
    clothes4 = clothes_factory(label=LaundryLabel.WASH, volume=0.01)
    order = order_factory(
        received_at=today,
        clothes_list=[clothes1, clothes2, clothes3, clothes4],
    )

    assert order.status == OrderState.PREPARING
    order_repo.add(order)
    session.commit()
    
    order_list = order_repo.get_by_status(status = OrderState.PREPARING)
    assert len(order_list) == 1

    laundrylabeldict = distribute_order(order_list)

    assert len(laundrylabeldict) == 2



########TODO
# @pytest.mark.skip()
def test_laundrybags_with_same_laundryLabel_allocated_into_same_laundrybag(session, 
                                                                           session_factory, 
                                                                           order_factory, 
                                                                           laundrybag_factory, 
                                                                           clothes_factory):
    # 새로운 주문(물세탁 빨래 volume 5) 추가.

    # uow = SqlAlchemyUnitOfWork(session_factory)

    # with uow :
    #     uow.orders.add(order_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 6)]))
    #     uow.laundrybags.add(laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 20)]))
    #     uow.commit()

    # with uow :
    #     allocate_laundrybag(uow)
    #     uow.commit()

    # assert len(uow.laundrybags.list()) == 2


#################
    order_repo = SqlAlchemyOrderRepository(session)    
    order_repo.add(order_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 6)]))
    session.commit()
    assert len(order_repo.list()) == 1
    # 기존의 LaundryBag(volume 20) 추가. max_volume 25. 
    laundrybag_repo = SqlAlchemyLaundryBagRepository(session)
    laundrybag_repo.add(laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 20)]))
    session.commit()
    assert len(order_repo.list()) == 1

    ## TODO [Order] : status를 Property로 바꾼 후, filter_by기능 작동 안함.
    order_list = order_repo.get_by_status(status = OrderState.PREPARING)
    assert len(order_list) == 1

    laundrylabeldict = distribute_order(order_list)
    assert len(list(laundrylabeldict.values())[0]) == 1 
    for laundrylabel, clothes_list in laundrylabeldict.items() :
        waiting_bag = laundrybag_repo.get_waitingbag_by_label(label = laundrylabel)

        for clothes in clothes_list :
            waiting_bag_list = put_clothes_in_laundrybag(waiting_bag, clothes)
            assert len(waiting_bag_list) == 5
            for waiting_bag in waiting_bag_list :
                laundrybag_repo.add(waiting_bag)
        session.commit()
    

    laundrybags_in_ready = laundrybag_repo.get_by_status(status = LaundryBagState.READY)
    assert len(laundrybags_in_ready) == 1
    assert len(laundrybag_repo.list()) == 2





def test_load_waiting_laundrybag(session, laundrybag_factory, clothes_factory) :
    
    
    laundrylabel = LaundryLabel.WASH
    # setup

    laundrybag_repo = SqlAlchemyLaundryBagRepository(session)
    clothes = clothes_factory(volume = 20, label = laundrylabel)
    laundrybag = laundrybag_factory(clothes_list = [clothes])

    laundrybag_repo.add(laundrybag)
    session.commit()
    

    # new clothes
    new_clothes = clothes_factory(volume = 10, label = laundrylabel)

    # load existing laundrybag
    waiting_bag = laundrybag_repo.get_waitingbag_by_label(laundrylabel)

    waiting_bag_list = put_clothes_in_laundrybag(waiting_bag, clothes)
    for waiting_bag in waiting_bag_list :
        laundrybag_repo.add(waiting_bag)

    session.commit()

    assert len(laundrybag_repo.get_by_status(status = LaundryBagState.COLLECTING)) == 1 and \
            len(laundrybag_repo.get_by_status(status = LaundryBagState.READY)) == 1 




@pytest.mark.skip()
def test_multiple_orders_distributed_into_laundrybags(session, order_factory, clothes_factory):
    multiple_orders = []
    label_options = [LaundryLabel.WASH, LaundryLabel.HAND]
    
    order_repo = SqlAlchemyOrderRepository(session)
    
    for i in range(2) :
        clothes_list = [clothes_factory(label = label_options[ i%2 ], volume = 3.0, received_at = today) for _ in range(9)]
        new_order = order_factory(orderid = f'order-{i}', clothes_list = clothes_list )
        multiple_orders.append(new_order)
        order_repo.add(new_order)
    session.commit()
    
    # load order, laundrybag repository
    assert  len(multiple_orders) == 2
    laundrybag_repo = SqlAlchemyLaundryBagRepository(session)

    order_list = order_repo.get_by_status(status = OrderState.SENDING)
    
    laundrylabeldict = distribute_order(order_list)

    for laundrylabel, clothes_list in laundrylabeldict.items() :
        waiting_bag = laundrybag_repo.get_waitingbag_by_label(label = laundrylabel)
        
        # if not waiting_bag :
        #     waiting_bag = LaundryBag(laundrybagid = f'bag-{laundrylabel}-{str(uuid4())[:2]}-0')

        for clothes in clothes_list :
            waiting_bag_list = put_clothes_in_laundrybag(waiting_bag, clothes)
            for waiting_bag in waiting_bag_list :
                laundrybag_repo.add(waiting_bag)
        session.commit()
    

    assert len(laundrybag_repo.list()) == 4 and len(multiple_orders) == 2



#################
# reclaim order #
#################

def test_clothes_finished_laundry_reclaim_by_orderid(session_factory, clothes_factory):
    orderid_list = ["EUNSUNG_o3_230715", "SAM_o18_230714", "LUKE_01_230716"]

    uow = SqlAlchemyUnitOfWork(session_factory)

    with uow :
        for i in range(len(orderid_list)):
            orderid = orderid_list[i]
            clothes_list = [clothes_factory(volume = 1) for _ in range(5)]
            for clothes in clothes_list:  # assign orderid to clothes
                clothes.orderid = orderid

            laundryBag = LaundryBag(laundrybagid = f'test-laundrybag_{i}', clothes_list = clothes_list, created_at=None)
            
            laundryBag.status = LaundryBagState.DONE

            ## TODO : better way to simulate to update laundry process DONE
            for clothes in laundryBag.clothes_list:
                clothes.status = ClothesState.DONE
            
            uow.laundrybags.add(laundryBag)
        uow.commit()
        assert len(uow.laundrybags.list()) == 3
        
        
        reclaimed_order_dict = reclaim_clothes_into_order(uow)
        uow.commit()

    assert all([clothes.status == ClothesState.RECLAIMED for clothes in uow.clothes.list()])
            