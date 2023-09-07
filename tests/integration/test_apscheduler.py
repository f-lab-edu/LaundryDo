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
    with uow_factory :
        print(uow_factory.machines.list())
    services.put_laundrybag_into_machine(uow_factory)    
    with uow_factory :
        assert len(uow_factory.machines.get_by_status(status = MachineState.READY)) == 10



# @pytest.mark.skip()
# @pytest.mark.parametrize('set_up_orders', [
#                             [[LaundryLabel.DRY], 1, 1],
                            
#                             ], 
#                          indirect= True)
def test_order_allocated_to_new_laundrybag(uow_factory, order_factory, laundrybag_factory, clothes_factory) :
    # register orders  
    order = order_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = MACHINE_MAXVOLUME)])
    with uow_factory :
        uow_factory.orders.add(order)
        uow_factory.commit()
    # there is no laundrybag in wait

    with uow_factory :
        laundrybag_list = uow_factory.laundrybags.()

        clothes_list = uow_factory.clothes.get_by_status(ClothesState.PREPARING)




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


    labels = [LaundryLabel.DRY]
    volume = MACHINE_MAXVOLUME 
    
    clothes_list = [clothes_factory(label = labels[i], volume = volume) for i in range(len(labels))]
    order = order_factory(clothes_list = clothes_list)
    
    with uow_factory :
        uow_factory.orders.add(order)
        uow_factory.commit()

        
        clothes_in_preparing = uow_factory.clothes.get_by_status(status = ClothesState.PREPARING)
        assert clothes_in_preparing == clothes_list
    
    services.allocate_laundrybag(uow_factory) ## order 조회에서 실패

    with uow_factory :
        assert uow_factory.laundrybags.list() is None
        assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.READY)) == 1

    num_laundrybag_in_ready = 3
    num_laundrybag_collecting = 4

    laundrybagstates = num_laundrybag_in_ready * [LaundryBagState.READY] \
                             + num_laundrybag_collecting * [LaundryBagState.COLLECTING]

    laundrybag_list = []
    with uow_factory :
        for i in range(len(laundrybagstates)) :
            laundrybag = laundrybag_factory(status = laundrybagstates[i])
            laundrybag_list.append(laundrybag)
            uow_factory.laundrybags.add(laundrybag)
        uow_factory.commit()
        
    services.put_laundrybag_into_machine(uow_factory)


    with uow_factory :
        assert len(uow_factory.laundrybags.get_by_status(status = LaundryBagState.RUNNING)) == num_laundrybag_in_ready
        assert len(uow_factory.machines.get_by_status(status = MachineState.RUNNING)) == num_laundrybag_in_ready




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

