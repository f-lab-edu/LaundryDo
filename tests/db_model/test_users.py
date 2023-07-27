from src.dbmodel import OrderState, ClothesState

def test_user_request_new_order(dbmodel_user_factory, dbmodel_order_factory):
    new_user = dbmodel_user_factory()
    new_order = dbmodel_order_factory()

    new_user.request_order(new_order)

    assert new_user.orderlist == [new_order]


def test_user_cancel_order(dbmodel_user_factory, dbmodel_order_factory):
    new_user = dbmodel_user_factory()
    new_order = dbmodel_order_factory()

    new_user.request_order(new_order)
    new_user.cancel_order(new_order)

    assert new_user.orderlist[new_user.orderlist.index(new_order)].status == OrderState.CANCELLED \
             and all([clothes.status == ClothesState.CANCELLED for clothes in new_order.clothes_list])


def test_user_request_order_status(dbmodel_user_factory, dbmodel_order_factory) :
    new_user = dbmodel_user_factory()
    new_order = dbmodel_order_factory()
    
    new_user.request_order(new_order)
    
    order_status = new_user.request_order_status(new_order)

    assert order_status == OrderState.PREPARING


def test_user_request_order_history(dbmodel_user_factory, dbmodel_order_factory) :
    new_user = dbmodel_user_factory()
    for i in range(10) :
        new_order = dbmodel_order_factory()
        new_user.request_order(new_order)

    assert len(new_user.request_order_history()) == 10
