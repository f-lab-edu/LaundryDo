from src.dbmodel import (
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



def test_user_create_orders(base_session, dbmodel_user_factory, dbmodel_order_factory) :
    user1 = dbmodel_user_factory()

    num_orders = 5
    for _ in range(num_orders) :
        user1.request_order(dbmodel_order_factory())

    base_session.add(user1)
    base_session.commit()

    assert len(base_session.query(Order).all()) == num_orders
    

def test_create_user(base_session) :
    base_session.execute(
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

    assert base_session.query(User).all() == expected




def test_create_order(base_session, dbmodel_order_factory) :
    order1 = dbmodel_order_factory()
    
    base_session.add(order1)
    base_session.commit()


    assert base_session.query(Order).one() == order1
            

def test_order_creation_also_create_clothes_rows(base_session, dbmodel_order_factory, dbmodel_clothes_factory) :
    order1 = dbmodel_order_factory(clothes_list = [dbmodel_clothes_factory() for _ in range(1)], status = OrderState.RECLAIMING)

    base_session.add(order1)
    base_session.commit()

    assert len(base_session.query(Order).all()) == 1
    assert len(base_session.query(Clothes).all()) == 1


def test_laundrybag(base_session, dbmodel_laundrybag_factory) :
    laundrybag = dbmodel_laundrybag_factory()

    base_session.add(laundrybag)
    base_session.commit()

    assert base_session.query(LaundryBag).one().status == LaundryBagState.COLLECTING and \
                all([clothes.status == ClothesState.DISTRIBUTED for clothes in base_session.query(Clothes).all()])
    

def test_machine_run_and_finish_laundry(base_session, dbmodel_laundrybag_factory) : 
    machine = Machine(machineid = 'test-machine')
    laundrybag = dbmodel_laundrybag_factory()

    machine.put(laundrybag)
    machine.start(datetime(2023, 7, 21, 10, 10))
    base_session.add(machine)
    base_session.commit()

    assert base_session.query(Machine).first().status == MachineState.RUNNING and \
            base_session.query(LaundryBag).first().status == LaundryBagState.RUN

    machine.stop(datetime(2023, 7, 21, 11, 10))
    base_session.add(machine)
    base_session.commit()

    assert base_session.query(Machine).first().status == MachineState.STOP and \
            base_session.query(LaundryBag).first().status == LaundryBagState.RUN