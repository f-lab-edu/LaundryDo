import pytest
from src.dbmodel import Machine, LaundryLabel, MachineState
from datetime import datetime, timedelta

def test_fail_to_machine_put_laundryBag_exceed_max_volume(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(volume = 10) for _ in range(5)])

    with pytest.raises(ValueError):
        machine1.put(laundryBag)




def test_machine_returns_requiredTime(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.put(laundryBag)

    assert machine1.requiredTime == 90




def test_machine_returns_runtime(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.put(laundryBag)
    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))

    assert machine1.get_runtime(exec_time = datetime(2023, 7, 14, 17, 50)) == timedelta(minutes = 50)




def test_machine_returns_remaining_time(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.put(laundryBag)
    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))

    assert machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 20)) == timedelta(minutes=70)


def test_machine_stop_and_resume_returns_remaining_time(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(label = LaundryLabel.WASH, volume = 3) for _ in range(5)])

    machine1.put(laundryBag)

    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))
    machine1.stop(exec_time=datetime(2023, 7, 14, 17, 5))
    assert machine1.status == MachineState.STOP and \
            machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 10)) == timedelta(minutes=90 - 5)

    machine1.resume(exec_time=datetime(2023, 7, 14, 17, 15))
    assert machine1.status == MachineState.RUNNING and \
        machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 20)) == timedelta(minutes=90 - 10)


def test_running_machine_stops_if_requiredTime_passed():
    # TODO : [Machine] continuous monitoring on machine state is required, maybe event listening...?
    # 시간 처리 방법
    pass


def test_fail_to_allocate_laundrybag_into_machine_if_broken_or_running(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    machine1 = Machine(machineid="TROMM1")
    laundryBag = dbmodel_laundrybag_factory(clothes_list=[dbmodel_clothes_factory(label = LaundryLabel.WASH, volume = 1) for _ in range(10)])

    machine1.status = MachineState.BROKEN

    with pytest.raises(ValueError):
        machine1.put(laundryBag)


def test_machine_is_empty_when_laundry_is_done() :
    ## ClothesState == 'DONE' and machine.contained is None and machine.MachineSta te == DONE
    pass
