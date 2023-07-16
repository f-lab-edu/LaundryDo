import random
from tabnanny import check
from uuid import uuid4
from venv import create

import pytest

from model import (
    Clothes,
    ClothesState,
    Order,
    LaundryLabel,
    LaundryBag,
    LaundryMachine,
    OrderState,
    User,
    MachineState,
    LAUNDRYBAG_MAXVOLUME,
)

from typing import List, Dict

from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)


# clothes, order, laundrybag, user


def divide_order(order_list: List[Order]) -> List[LaundryBag]:
    laundrylabeldict = {}

    for order in order_list:
        for clothes in order:
            if clothes.label in laundrylabeldict:
                laundrylabeldict[clothes.label].append(clothes)
            else:
                laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict


def put_in_laundrybag(laundryBagDict: Dict[LaundryLabel, List[Clothes]]):

    # sortlaundryBagDict = {}
    laundryBagList = []
    for laundrylabel, clothes_list in laundryBagDict.items():
        # sort by date
        clothes_list.sort()

        # split clothes_list by max volume

        laundryBag = LaundryBag(clothes_list=[], createdTime=datetime.now())

        while clothes_list:
            clothes = clothes_list.pop()
            if clothes.volume + laundryBag.volumeContained <= LAUNDRYBAG_MAXVOLUME:
                laundryBag.append(clothes)
            else:
                laundryBagList.append(laundryBag)
                laundryBag = LaundryBag(
                    clothes_list=[clothes], createdTime=datetime.now()
                )

        # sortlaundryBagDict[laundrylabel] = laundryBagQueue

    return laundryBagList


def reclaim_clothes_into_order(laundryBag_list: List[LaundryBag]) -> List[Order]:
    assert all(
        [
            clothes.status == ClothesState.DONE
            for laundryBag in laundryBag_list
            for clothes in laundryBag
        ]
    )

    reclaimed_dict = {}

    for laundryBag in laundryBag_list:
        for clothes in laundryBag:
            clothes.status = ClothesState.RECLAIMED
            if clothes.orderid not in reclaimed_dict:
                reclaimed_dict[clothes.orderid] = [clothes]
            else:
                reclaimed_dict[clothes.orderid].append(clothes)

    reclaimed_list = []
    for orderid, reclaimed in reclaimed_dict.items():
        reclaimed_list.append(
            Order(id=orderid, clothes_list=reclaimed, status=OrderState.RECLAIMING)
        )

    return reclaimed_list


def check_clothes_in_order_is_fully_reclaimed(order: Order):
    for clothes in order:
        if clothes.status != ClothesState.RECLAIMED:
            return False
    return True


def change_order_status(order: Order):
    if check_clothes_in_order_is_fully_reclaimed(order):
        order.status = OrderState.SHIP_READY


def new_clothes(label=None, volume=None, status=None):

    id = str(uuid4())[:4]
    if label is None:
        label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

    if volume is None:
        volume = random.randint(5, 15)
    if status is None:
        status = random.choice(
            [
                ClothesState.PREPARING,
                ClothesState.CANCELLED,
                ClothesState.DIVIDED,
                ClothesState.PROCESSING,
                ClothesState.DONE,
            ]
        )
    return Clothes(id=id, label=label, volume=volume, status=status)


###########
# Clothes #
###########


def test_sort_clothes_by_time():
    clothes_today = Clothes(
        id="green top", volume=0.3, label=LaundryLabel.WASH, received_at=today
    )
    clothes_yesterday = Clothes(
        id="blue jean", volume=0.4, label=LaundryLabel.WASH, received_at=yesterday
    )
    clothes_longtimeago = Clothes(
        id="yellow skirt", volume=0.7, label=LaundryLabel.WASH, received_at=longtimeago
    )

    assert sorted([clothes_yesterday, clothes_longtimeago, clothes_today]) == [
        clothes_longtimeago,
        clothes_yesterday,
        clothes_today,
    ]


########
# User #
########
def test_user_request_new_order(new_user, new_order):
    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(new_user, new_order):

    new_user.request_order(new_order)

    new_user.cancel_order(new_order)

    assert new_user.orderlist == []


#############
#   Order   #
#############
def test_clothes_in_an_order_has_all_same_order_id(new_order):

    assert len(set(order.orderid for order in new_order)) == 1


def test_order_sort_by_laundrybags():
    clothes1 = Clothes(id=str(uuid4())[:4], label=LaundryLabel.WASH, volume=0.3)
    clothes2 = Clothes(id=str(uuid4())[:4], label=LaundryLabel.DRY, volume=0.3)
    clothes3 = Clothes(id=str(uuid4())[:4], label=LaundryLabel.DRY, volume=0.3)
    clothes4 = Clothes(id=str(uuid4())[:4], label=LaundryLabel.WASH, volume=0.3)
    order = Order(
        "order1",
        received_at=today,
        clothes_list=[clothes1, clothes2, clothes3, clothes4],
    )

    laundrylabeldict = divide_order([order])

    assert len(laundrylabeldict) == 2


def test_multiple_orders_divided_into_laundrybags(new_order):
    multiple_orders = [new_order for _ in range(10)]


##############
# LaundryBag #
##############


def test_laundrybag_clothes_status_changed_to_divided():
    laundryBag = LaundryBag([new_clothes() for _ in range(10)], createdTime=today)

    assert all([clothes.status == ClothesState.DIVIDED for clothes in laundryBag])


def test_laundrybags_with_same_laundryLabel_combine_into_same_laundrybag(new_order):
    laundrylabeldict = divide_order([new_order])
    laundryBagList = put_in_laundrybag(laundrylabeldict)

    for laundryBag in laundryBagList:
        assert len(set(clothes.label for clothes in laundryBag)) == 1


def test_laundrybags_sorted_by_time():
    longtimeago_laundryBag = LaundryBag(
        [new_clothes() for _ in range(10)], createdTime=longtimeago
    )
    yesterday_laundryBag = LaundryBag(
        [new_clothes() for _ in range(10)], createdTime=yesterday
    )
    today_laundryBag = LaundryBag([new_clothes() for _ in range(10)], createdTime=today)

    assert sorted([today_laundryBag, yesterday_laundryBag, longtimeago_laundryBag]) == [
        longtimeago_laundryBag,
        yesterday_laundryBag,
        today_laundryBag,
    ]


##################
# LaundryMachine #
##################


def test_fail_to_laundryMachine_put_laundryBag_exceed_max_volume():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag([new_clothes() for _ in range(5)], createdTime=today)

    with pytest.raises(ValueError):
        machine1.putLaundryBag(laundryBag)


def test_laundryMachine_returns_requiredTime():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag(
        [new_clothes(label=LaundryLabel.WASH, volume=3) for _ in range(5)],
        createdTime=today,
    )

    machine1.putLaundryBag(laundryBag)

    assert machine1.requiredTime == 90


def test_laundryMachine_returns_runtime():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag(
        [new_clothes(label=LaundryLabel.WASH, volume=3) for _ in range(5)],
        createdTime=today,
    )

    machine1.putLaundryBag(laundryBag)

    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))

    ## TODO : laundryMachine needs to update runtime in
    pass


def test_laundryMachine_returns_remaining_time():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag(
        [new_clothes(label=LaundryLabel.WASH, volume=3) for _ in range(5)],
        createdTime=today,
    )

    machine1.putLaundryBag(laundryBag)

    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))

    assert machine1.remainingTime(exec_time=datetime(2023, 7, 14, 17, 20)) == timedelta(
        minutes=70
    )


def test_laundryMachine_stop_and_resume_returns_remaining_time():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag(
        [new_clothes(label=LaundryLabel.WASH, volume=3) for _ in range(5)],
        createdTime=today,
    )

    machine1.putLaundryBag(laundryBag)

    machine1.start(exec_time=datetime(2023, 7, 14, 17, 0))
    machine1.stop(exec_time=datetime(2023, 7, 14, 17, 5))
    assert machine1.status == MachineState.STOP and machine1.remainingTime(
        exec_time=datetime(2023, 7, 14, 17, 10)
    ) == timedelta(minutes=90 - 5)

    machine1.resume(exec_time=datetime(2023, 7, 14, 17, 15))
    assert machine1.status == MachineState.RUNNING and machine1.remainingTime(
        exec_time=datetime(2023, 7, 14, 17, 20)
    ) == timedelta(minutes=90 - 10)


def test_running_laundryMachine_stops_if_requiredTime_passed():
    # TODO : continuous monitoring on laundrymachine state is required, maybe event listening...?
    pass


def test_fail_to_allocate_laundrybag_into_laundryMachine_if_broken_or_running():
    machine1 = LaundryMachine(id="TROMM1")
    laundryBag = LaundryBag([new_clothes() for _ in range(5)], createdTime=today)

    machine1.status = MachineState.BROKEN

    with pytest.raises(ValueError):
        machine1.putLaundryBag(laundryBag)


def test_laundryMachine_is_empty_when_laundry_is_done():
    ## ClothesState == 'DONE' and laundryMachine.contained is None and laundryMachine.MachineState == DONE
    pass


## TODO : run on multiple laundryjob cycles

#################
# reclaim order #
#################


def test_clothes_finished_laundry_reclaim_by_orderid():
    orderid_list = ["EUNSUNG_o3_230715", "SAM_o18_230714", "LUKE_01_230716"]

    freshly_done_laundrybags = []

    for i in range(len(orderid_list)):
        orderid = orderid_list[i]
        clothes_list = [new_clothes() for _ in range(5)]
        for clothes in clothes_list:  # assign orderid to clothes
            clothes.orderid = orderid

        laundryBag = LaundryBag(clothes_list, createdTime=None)
        for clothes in laundryBag:
            clothes.status = ClothesState.DONE
        freshly_done_laundrybags.append(laundryBag)

    reclaimed_order_list = reclaim_clothes_into_order(freshly_done_laundrybags)

    assert set([order.id for order in reclaimed_order_list]) == set(orderid_list)


def test_check_every_clothes_by_orderid_reclaimed():
    pass
