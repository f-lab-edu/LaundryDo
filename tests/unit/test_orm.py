from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    LaundryBag,
    Machine
)

def test_user_create_orders(session, user_factory, order_factory) :
    user1 = user_factory()

    num_orders = 5
    for _ in range(num_orders) :
        user1.request_order(order_factory())

    session.add(user1)
    session.commit()

    assert session.query(Order).all() == [user_factory()]
        # len(session.query(Order).all()) == num_orders
    

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


    assert session.query(Order).one().orderid == "test-order" 
            

# def test_order_creation_also_create_clothes_rows(session, order_factory, clothes_factory) :
#     order1 = order_factory(clothes_list = [clothes_factory() for _ in range(1)], status = OrderState.RECLAIMING)


#     session.add(order1)
#     session.commit()


#     assert len(session.query(Clothes).all()) == 1


def test_create_clothes(session) :
    pass

