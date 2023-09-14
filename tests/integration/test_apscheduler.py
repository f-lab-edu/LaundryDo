from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from src.application import LaundryBagManager
from src.domain import Machine, MachineState, LaundryBagState, LaundryLabel, OrderState, ClothesState
from src.domain.spec import MACHINE_MAXVOLUME

from typing import List
import pytest

'''
apscheduler jobs
1. put laundrybag(state == READY) into machine(state == READY)
2. reclaim clothes from machine(state == DONE)
3. check if order(state == RECLAIMING) is fully reclaimed(clothes == RECLAIMED in clothes_list), and change Orderstate = SHIP_READY
4. ship order(state == SHIP_READY) == SHIP
'''

@pytest.fixture()
def set_up_machines(uow_factory) :
    '''set up laundry machines in READY state'''
    with uow_factory :
        for i in range(10) :
            machine = Machine(machineid = f'test-machine{i}')
            uow_factory.machines.add(machine)
        uow_factory.commit()



##################################################################
# 1. put laundrybag(state == READY) into machine(state == READY) #
##################################################################

def test_NO_laundrybag_is_ready_for_laundry(set_up_machines, uow_factory) :
    services.allocate_laundrybag_to_machine(uow_factory)    
    with uow_factory :
        assert len(uow_factory.machines.get_by_status(status = MachineState.READY)) == 10

def test_NO_Machine_is_available_for_laundrybag(uow_factory, laundrybag_factory) :
    # No machine available
    with uow_factory :
        assert uow_factory.machines.list() == []

    new_lb = laundrybag_factory()
    with uow_factory :
        uow_factory.laundrybags.add(new_lb)
        uow_factory.commit()

    services.allocate_laundrybag_to_machine(uow_factory)

    with uow_factory :
        assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.COLLECTING)) == 1
        assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.RUNNING)) == 0


    

def test_laundrybag_put_on_machine(set_up_machines, laundrybag_factory, clothes_factory, uow_factory) :
    num_laundrybags = 5
    with uow_factory :
        for _ in range(num_laundrybags) :
            # 라벨 고정. 빨래 volume 최대(=> 바로 laundrybag 상태 READY 변경). 머신에 정상적으로 들어가고 작동하는지만 확인한다
            clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 25)] 
            laundrybag = laundrybag_factory(clothes_list = clothes_list)
            uow_factory.laundrybags.add(laundrybag)
        uow_factory.commit()

    services.allocate_laundrybag_to_machine(uow_factory)

    
    with uow_factory :
        # Laundrybag status 확인
        laundrybags = uow_factory.laundrybags.list()
        assert all([lb.status == LaundryBagState.RUNNING for lb in laundrybags])
    
        # Machine status RUN 갯수 == 5 
        assert len(uow_factory.machines.get_by_status(MachineState.RUNNING)) == num_laundrybags



def test_order_allocated_to_new_laundrybag(uow_factory, order_factory, laundrybag_factory, clothes_factory) :
    # register orders  
    with uow_factory :
        for label in LaundryLabel.__members__ :
            order = order_factory(clothes_list = [clothes_factory(label = label, volume = MACHINE_MAXVOLUME)])
            uow_factory.orders.add(order)
        uow_factory.commit()
    # there is no laundrybag in wait

    services.allocate_clothes_in_laundrybag(uow_factory)
    
    # 라벨이 서로 다른 laundrybag을 3개 만든다.
    with uow_factory :
        assert len(uow_factory.laundrybags.list()) == 3





@pytest.mark.skip()
def test_laundrybag_ready_for_laundry_put_in_machine(set_up_machines, uow_factory, order_factory, laundrybag_factory, clothes_factory) :
    ''' 
    check
    1. laundrybag state 
    2. machine state
    3. order state
    4. clothes state
    '''
    # set up machines : 10 in ready
    # set up laundrybags in ready
    pass

    # labels = [LaundryLabel.DRY]
    # volume = MACHINE_MAXVOLUME 
    
    # clothes_list = [clothes_factory(label = labels[i], volume = volume) for i in range(len(labels))]
    # order = order_factory(clothes_list = clothes_list)
    
    # with uow_factory :
    #     uow_factory.orders.add(order)
    #     uow_factory.commit()

        
    #     clothes_in_preparing = uow_factory.clothes.get_by_status(status = ClothesState.PREPARING)
    #     assert clothes_in_preparing == clothes_list
    
    # # services.allocate_laundrybag(uow_factory) ## order 조회에서 실패

    # with uow_factory :
    #     assert uow_factory.laundrybags.list() is None
    #     assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.READY)) == 1

    # num_laundrybag_in_ready = 3
    # num_laundrybag_collecting = 4

    # laundrybagstates = num_laundrybag_in_ready * [LaundryBagState.READY] \
    #                          + num_laundrybag_collecting * [LaundryBagState.COLLECTING]

    # laundrybag_list = []
    # with uow_factory :
    #     for i in range(len(laundrybagstates)) :
    #         laundrybag = laundrybag_factory(status = laundrybagstates[i])
    #         laundrybag_list.append(laundrybag)
    #         uow_factory.laundrybags.add(laundrybag)
    #     uow_factory.commit()
        
    # services.allocate_laundrybag_to_machine(uow_factory)


    # with uow_factory :
    #     assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.RUNNING)) == num_laundrybag_in_ready
    #     assert len(uow_factory.machines.get_by_status(status = MachineState.RUNNING)) == num_laundrybag_in_ready




##################################################
# 2. reclaim clothes from machine(state == DONE) #
##################################################
def test_NO_machine_is_finished() :
    pass

def test_machine_finished_time_match_the_expect_time() :
    pass

def test_clothes_state_changes_as_machine_finished_laundry() :
    pass

def test_laundrybag_state_changes_as_machine_finished_laundry() :
    pass

def test_order_state_changes_as_machine_finished_laundry() :
    pass

###################################################################################################
# 3. check if order(state == RECLAIMING) is fully reclaimed(clothes == RECLAIMED in clothes_list) #
###################################################################################################
def test_NO_order_is_fully_reclaimed() :
    pass

def test_clothes_state_changes_as_order_is_fully_reclaimed() :
    pass

def test_order_state_changes_as_order_is_fully_reclaimed() :
    pass

##############################################
# 4. ship order(state == SHIP_READY) == SHIP #
##############################################

# services.update_orderstate_fully_reclaimed()
# services.ship()
def test_NO_order_is_ready_to_be_shipped() :
    pass

def test_order_state_changes_as_ready_to_be_shipped() :
    pass

