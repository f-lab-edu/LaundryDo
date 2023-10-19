from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    ClothesState,
    LaundryBag,
    LaundryBagState,
    Machine,
    MachineState,
    LaundryLabel
)

from sqlalchemy.sql import text
from datetime import datetime, timedelta
from freezegun import freeze_time


def test_user_create_orders(session, user_factory, order_factory) :
    user1 = user_factory()

    num_orders = 5
    for i in range(num_orders) :
        user1.request_order(order_factory())
    
    session.add(user1)
    session.commit()

    assert len(session.query(Order).all()) == num_orders
    

def test_create_user(session) :
    session.execute(
        text(
        'INSERT INTO user (userid, address, password, phone_number) VALUES '
        '("user123", "서울시 중랑구", "test-password", "test-phonenum"),'
        '("user456", "서울시 동작구", "test-password", "test-phonenum"),'
        '("user789", "서울시 마포구", "test-password", "test-phonenum")'
            )
        )
    expected = [
        User("user123", "서울시 중랑구", "test-password", "test-phonenum"),
        User("user456", "서울시 동작구", "test-password", "test-phonenum"),
        User("user789", "서울시 마포구", "test-password", "test-phonenum")
    ]

    assert session.query(User).all() == expected




def test_create_order(session, order_factory) :
    order1 = order_factory()
    
    session.add(order1)
    session.commit()


    assert session.query(Order).one() == order1
            

def test_order_creation_also_create_clothes_rows(session, order_factory, clothes_factory) :
    order1 = order_factory(clothes_list = [clothes_factory() for _ in range(1)])#, status = OrderState.RECLAIMING)
    order1.status = OrderState.RECLAIMING
    session.add(order1)
    session.commit()

    assert len(session.query(Order).all()) == 1
    assert len(session.query(Clothes).all()) == 1


def test_laundrybag(session, laundrybag_factory) :
    laundrybag = laundrybag_factory()

    session.add(laundrybag)
    session.commit()

    assert session.query(LaundryBag).one().status == LaundryBagState.COLLECTING and \
                all([clothes.status == ClothesState.DISTRIBUTED for clothes in session.query(Clothes).all()])
    

def test_machine_run_and_finish_laundry(session, laundrybag_factory, clothes_factory) : 
    machine = Machine(machineid = 'test-machine')

    # 5 clothes with volume 1 & HAND label => require 100minutes to launder
    laundrybag = laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.HAND, volume = 1) for _ in range(5)])
    
    with freeze_time('2023-07-21 10:10:00') :
        machine.start(laundrybag)
    session.add(machine)
    session.commit()

    assert session.query(Machine).first().status == MachineState.RUNNING and \
            session.query(LaundryBag).first().status == LaundryBagState.RUNNING

    with freeze_time('2023-07-21 10:10:00', tz_offset=timedelta(hours = 1)) : # suppose to run 100 minutes. 1 hour passed.
        machine.stop()
    session.add(machine)
    session.commit()

    assert session.query(Machine).filter_by(machineid = machine.machineid).one().status == MachineState.STOP and \
            session.query(LaundryBag).first().status == LaundryBagState.RUNNING
    
    ## TODO status changed by remainingTime
    # with freeze_time('2023-07-21 11:50:00') : # suppose to run 100 minutes
    #     machine.stop()
    # session.add(machine)
    # session.commit()