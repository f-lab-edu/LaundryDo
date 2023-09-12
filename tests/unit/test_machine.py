import pytest


from src.domain import Machine, LaundryLabel, MachineState
from src.domain.machine import MaximumVolumeExceedError, BrokenError, AlreadyRunningError
from datetime import datetime, timedelta
from freezegun import freeze_time


# 머신에서 용량을 체크하기 전에, laundrybag 용량은 커지면 자동으로 나눠진다.
# def test_machine_fail_to_put_laundrybag_exceeding_max_volume(laundrybag_factory, clothes_factory):
#     machine1 = Machine(machineid="TROMM1")
#     laundryBag = laundrybag_factory(clothes_list=[clothes_factory(volume = 10, label = LaundryLabel.WASH) for _ in range(5)])
#     with pytest.raises(MaximumVolumeExceedError):
    #     machine1.start(laundryBag)

def test_machine_fail_to_resume_when_already_running(laundrybag_factory, clothes_factory) :
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory()])

    machine1.start(laundryBag)

    with pytest.raises(AlreadyRunningError) :
        machine1.resume()



def test_machine_sorted_by_lastupdate_time(laundrybag_factory, clothes_factory) :
    exectime = datetime.now()
    less_recently_used_machine = Machine(machineid = 'rested_more_machine')
    recently_used_machine = Machine(machineid = 'tired_machine')
    currently_running_machine_more_remaining_time = Machine(machineid = 'busy_machine_with_more_time_remaining')
    currently_running_machine_less_remaining_time = Machine(machineid = 'busy_machine_with_less_time_remaining')


    less_recently_used_machine.lastupdateTime = exectime - timedelta(minutes = 20)
    recently_used_machine.lastupdateTime = exectime

    assert less_recently_used_machine.status == MachineState.READY
    assert recently_used_machine.status == MachineState.READY

    bag1 = laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.DRY)])
    bag2 = laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.DRY)])

    with freeze_time(datetime.now()) :
        currently_running_machine_less_remaining_time.start(bag1)
    with freeze_time(datetime.now(), tz_offset = timedelta(minutes= 39)) :
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

    assert machine1.requiredTime == timedelta(minutes = 90)



def test_machine_returns_runtime(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    with freeze_time('2023-09-04 14:00:00') :
        machine1.start(laundryBag)
    assert machine1.status == MachineState.RUNNING

    with freeze_time('2023-09-04 14:00:00', tz_offset= timedelta(minutes = 50)) :
        assert machine1.runtime == timedelta(minutes = 50)




def test_machine_returns_remaining_time(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])
    
    with freeze_time('2023-07-14 17:00:00') :
        machine1.start(laundryBag)

    assert machine1.requiredTime == timedelta(minutes = 90) # 90 minutes for laundrylabel wash in volume 3.
    with freeze_time('2023-07-14 17:00:00', tz_offset=timedelta(minutes = 20)) :
        assert machine1.remainingTime == timedelta(minutes=70)


def test_machine_stop_and_resume_returns_remaining_time(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    with freeze_time('2023-07-14 17:00:00') :
        machine1.start(laundryBag)
    
    with freeze_time('2023-07-14 17:05:00') : # stop after 5 minutes
        machine1.stop()
    assert machine1.status == MachineState.STOP and \
            machine1.remainingTime == timedelta(minutes=90 - 5)

    with freeze_time('2023-07-14 17:15:00') :
        machine1.resume()

    with freeze_time('2023-07-14 17:15:00', tz_offset = timedelta(minutes = 5)) :
        assert machine1.status == MachineState.RUNNING and \
            machine1.remainingTime == timedelta(minutes=90 - 10) # ran total 5 minutes



def test_fail_to_allocate_laundrybag_into_machine_if_broken_or_running(laundrybag_factory, clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = laundrybag_factory(clothes_list=[clothes_factory(label = LaundryLabel.WASH, volume = 1) for _ in range(10)])

    machine1.status = MachineState.BROKEN

    with pytest.raises(BrokenError):
        machine1.start(laundryBag)


def test_running_machine_stops_if_requiredTime_passed():
    # TODO : [Machine] continuous monitoring on machine state is required, maybe event listening...?
    # 시간 처리 방법
    pass


def test_machine_is_empty_when_laundry_is_done() :
    ## ClothesState == 'DONE' and machine.contained is None and machine.MachineSta te == DONE
    pass
