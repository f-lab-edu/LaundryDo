from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from src.application import LaundryBagManager
from src.domain import Machine, MachineState, LaundryBagState, LaundryLabel, OrderState, ClothesState
from src.domain.spec import MACHINE_MAXVOLUME

from datetime import datetime, timedelta
from freezegun import freeze_time
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




def test_update_machine_state_if_laundry_done(uow_factory, laundrybag_factory, clothes_factory) :

    currtime = datetime.fromisoformat('2023-09-18 18:00:00')

    machine = Machine(machineid = 'TROMM1')
    clothes_list = [clothes_factory(volume = 3, label = LaundryLabel.DRY) for _ in range(3)] # 빨래시간 80분 소요
    laundrybag = laundrybag_factory(clothes_list = clothes_list)
    with freeze_time(currtime) :
        with uow_factory :
            uow_factory.laundrybags.add(laundrybag)
            machine.start(laundrybag)
            uow_factory.machines.add(machine)
            uow_factory.commit()

    with freeze_time(currtime, tz_offset = timedelta(minutes = 80)) : # supposed to be finished
        services.update_machine_state_if_laundry_done(uow_factory)

    with uow_factory :
        assert len(uow_factory.machines.get_by_status(MachineState.DONE)) == 1
        assert len(uow_factory.laundrybags.get_by_status(LaundryBagState.DONE)) == 1



def test_reclaim_clothes_from_machine(uow_factory, laundrybag_factory, clothes_factory) :
    currtime = datetime.fromisoformat('2023-09-18 18:00:00')

    machine = Machine(machineid = 'TROMM1')
    clothes_list = [clothes_factory(volume = 3, label = LaundryLabel.DRY) for _ in range(3)] # 빨래시간 80분 소요
    laundrybag = laundrybag_factory(clothes_list = clothes_list)
    with freeze_time(currtime) :
        with uow_factory :
            uow_factory.laundrybags.add(laundrybag)
            machine.start(laundrybag)
            uow_factory.machines.add(machine)
            uow_factory.commit()

    with freeze_time(currtime, tz_offset = timedelta(minutes = 80)) : # supposed to be finished
        services.update_machine_state_if_laundry_done(uow_factory)
    
    services.reclaim_clothes_from_machine(uow_factory)

    with uow_factory :
        assert len(uow_factory.clothes.get_by_status(ClothesState.RECLAIMED)) == 3
        assert len(uow_factory.laundrybags.get_by_status(LaundryBagState.COLLECTING)) == 1
        assert len(uow_factory.machines.get_by_status(MachineState.READY)) == 1
            




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

