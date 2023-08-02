from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    ClothesState,
    LaundryBag,
    LaundryBagState,
    Machine,
    MachineState
)

from datetime import datetime



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
        'INSERT INTO user (userid, address) VALUES '
        '("user123", "서울시 중랑구"),'
        '("user456", "서울시 동작구"),'
        '("user789", "서울시 마포구")'
    )

    expected = [
        User("user123", "서울시 중랑구"),
        User("user456", "서울시 동작구"),
        User("user789", "서울시 마포구")
    ]

    assert session.query(User).all() == expected




def test_create_order(session, order_factory) :
    order1 = order_factory()
    
    session.add(order1)
    session.commit()


    assert session.query(Order).one() == order1
            

def test_order_creation_also_create_clothes_rows(session, order_factory, clothes_factory) :
    order1 = order_factory(clothes_list = [clothes_factory() for _ in range(1)], status = OrderState.RECLAIMING)

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
    

def test_machine_run_and_finish_laundry(session, laundrybag_factory) : 
    machine = Machine(machineid = 'test-machine')
    laundrybag = laundrybag_factory()

    machine.start(laundrybag, datetime(2023, 7, 21, 10, 10))
    session.add(machine)
    session.commit()

    assert session.query(Machine).first().status == MachineState.RUNNING and \
            session.query(LaundryBag).first().status == LaundryBagState.RUNNING

    machine.stop(datetime(2023, 7, 21, 11, 10))
    session.add(machine)
    session.commit()

    assert session.query(Machine).first().status == MachineState.STOP and \
            session.query(LaundryBag).first().status == LaundryBagState.RUNNING