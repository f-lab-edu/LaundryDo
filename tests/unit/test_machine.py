import pytest

from pytest import MonkeyPatch
from src.domain import Machine, LaundryLabel, MachineState
from src.domain.machine import MaximumVolumeExceedError, BrokenError, AlreadyRunningError
from datetime import datetime, timedelta

def test_machine_fail_to_put_laundrybag_exceeding_max_volume(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(volume = 10) for _ in range(5)])

    with pytest.raises(MaximumVolumeExceedError):
        machine1.start(laundryBag)

def test_machine_fail_to_resume_when_already_running(laundrybag_factory) :
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory()

    machine1.start(laundryBag)

    with pytest.raises(AlreadyRunningError) :
        machine1.resume()



def test_machine_sorted_by_lastupdate_time(laundrybag_factory, clothes_factory) :
    exectime = datetime.now()

    less_recently_used_machine = Machine(machineid = 'rested_more_machine')
    recently_used_machine = Machine(machineid = 'tired_machine')
    currently_running_machine_more_remaining_time = Machine(machineid = 'busy_machine_with_more_time_remaining')
    currently_running_machine_less_remaining_time = Machine(machineid = 'busy_machine_with_less_time_remaining')


    less_recently_used_machine.lastupdateTime = exectime - timedelta(minutes = 30)
    recently_used_machine.lastupdateTime = exectime

    bag1 = laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.DRY)])
    bag2 = laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.DRY)])

    currently_running_machine_less_remaining_time.start(bag1)
    currently_running_machine_more_remaining_time.start(bag2)
    
    
    

    assert currently_running_machine_less_remaining_time.status == MachineState.RUNNING and \
            currently_running_machine_more_remaining_time.status == MachineState.RUNNING


    assert sorted([recently_used_machine, 
                   currently_running_machine_more_remaining_time, 
                   currently_running_machine_less_remaining_time,
                   less_recently_used_machine ]) == [less_recently_used_machine,
                                                     recently_used_machine,
                                                     currently_running_machine_less_remaining_time,
                                                     currently_running_machine_more_remaining_time
                                                     ]
    


def test_machine_returns_requiredTime(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.start(laundryBag)

    assert machine1.requiredTime == 90




def test_machine_returns_runtime(laundrybag_factory, clothes_factory):
    datetime.now.return_value = datetime(2023, 7, 14, 17, 50)
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.start(laundryBag)
    assert machine1.status == MachineState.RUNNING
    machine1.start_time = datetime(2023, 7, 14, 17, 0)


    assert machine1.get_runtime() == timedelta(minutes = 50)




def test_machine_returns_remaining_time(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.start(laundryBag, exec_time=datetime(2023, 7, 14, 17, 0))

    assert machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 20)) == timedelta(minutes=70)


def test_machine_stop_and_resume_returns_remaining_time(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.start(laundryBag, exec_time=datetime(2023, 7, 14, 17, 0))
    machine1.stop(exec_time=datetime(2023, 7, 14, 17, 5))
    assert machine1.status == MachineState.STOP and \
            machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 10)) == timedelta(minutes=90 - 5)

    machine1.resume(exec_time=datetime(2023, 7, 14, 17, 15))
    assert machine1.status == MachineState.RUNNING and \
        machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 20)) == timedelta(minutes=90 - 10)



def test_fail_to_allocate_laundrybag_into_machine_if_broken_or_running(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 1) for _ in range(10)])

    machine1.status = MachineState.BROKEN

    with pytest.raises(BrokenError):
        machine1.start(laundryBag, datetime.now())


def test_running_machine_stops_if_requiredTime_passed():
    # TODO : [Machine] continuous monitoring on machine state is required, maybe event listening...?
    # 시간 처리 방법
    pass


def test_machine_is_empty_when_laundry_is_done() :
    ## ClothesState == 'DONE' and machine.contained is None and machine.MachineSta te == DONE
    pass
