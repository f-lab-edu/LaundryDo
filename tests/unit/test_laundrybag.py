from src.domain import distribute_order, put_in_laundrybag, ClothesState
from datetime import datetime, timedelta


today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)

def test_laundrybag_clothes_status_changed_to_distributed(laundrybag_factory, clothes_factory):
    laundryBag = laundrybag_factory(clothes_list = [clothes_factory() for _ in range(10)])

    assert all([clothes.status == ClothesState.DISTRIBUTED for clothes in laundryBag])


def test_laundrybags_with_same_laundryLabel_combine_into_same_laundrybag(order_factory):
    laundrylabeldict = distribute_order([order_factory() for _ in range(10)])
    laundryBagList = put_in_laundrybag(laundrylabeldict)

    for laundryBag in laundryBagList:
        assert len(set(clothes.label for clothes in laundryBag)) == 1


def test_laundrybags_sorted_by_time(laundrybag_factory):
    longtimeago_laundryBag = laundrybag_factory(createdTime= longtimeago)
    yesterday_laundryBag = laundrybag_factory(createdTime= yesterday)
    today_laundryBag = laundrybag_factory(createdTime= today)

    assert sorted([today_laundryBag, yesterday_laundryBag, longtimeago_laundryBag]) \
                == [longtimeago_laundryBag, yesterday_laundryBag, today_laundryBag,]

