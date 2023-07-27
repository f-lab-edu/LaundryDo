from src.domain import (
    LaundryLabel, 
    LaundryBagState,
    ClothesState, 
    LaundryBag, 
)



from datetime import datetime

today = datetime.today()

def test_clothes_in_an_order_has_all_same_order_id(order_factory, clothes_factory):

    new_order = order_factory(clothes_list = [clothes_factory() for _ in range(10)])
    assert len(set(order.orderid for order in new_order.clothes_list)) == 1



def test_multiple_orders_with_same_label_and_over_max_volume_distributed_into_laundrybags(order_factory, clothes_factory) :
    pass



def test_check_every_clothes_by_orderid_reclaimed():
    pass