from src.domain import OrderState, ClothesState

def test_user_request_new_order(user_factory, order_factory):
    new_user = user_factory()
    new_order = order_factory()

    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(user_factory, order_factory):
    new_user = user_factory()
    new_order = order_factory()

    new_user.request_order(new_order)
    new_user.cancel_order(new_order)

    assert new_user.orderlist[new_user.orderlist.index(new_order)].status == OrderState.CANCELLED \
             and all([clothes.status == ClothesState.CANCELLED for clothes in new_order.clothes_list])


def test_user_request_order_status(user_factory, order_factory) :
    new_user = user_factory()
    new_order = order_factory()
    
    new_user.request_order(new_order)
    
    order_status = new_user.request_order_status(new_order)

    assert order_status == OrderState.SENDING


def test_user_request_order_history(user_factory, order_factory) :
    new_user = user_factory()
    for i in range(10) :
        new_order = order_factory()
        new_user.request_order(new_order)

    assert len(new_user.request_order_history()) == 10
