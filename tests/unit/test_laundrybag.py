from src.domain import ClothesState, LaundryLabel, LaundryBagState
from datetime import datetime, timedelta
from freezegun import freeze_time


today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)

def test_laundrybag_clothes_status_changed_to_distributed(laundrybag_factory, clothes_factory):
    laundryBag = laundrybag_factory(clothes_list = [clothes_factory() for _ in range(10)])

    assert laundryBag.clothes_list[0].status == ClothesState.DISTRIBUTED
    assert all([clothes.status == ClothesState.DISTRIBUTED for clothes in laundryBag.clothes_list])


def test_laundrybags_sorted_by_time(laundrybag_factory):

    with freeze_time(longtimeago) :
        longtimeago_laundryBag = laundrybag_factory()
    with freeze_time(yesterday) :
        yesterday_laundryBag = laundrybag_factory()
    with freeze_time(today) :
        today_laundryBag = laundrybag_factory()

    assert sorted([today_laundryBag, yesterday_laundryBag, longtimeago_laundryBag]) \
                == [longtimeago_laundryBag, yesterday_laundryBag, today_laundryBag,]

def test_laundrybag_label_changed_as_clothes_comes_in(laundrybag_factory, clothes_factory) :

    laundrybag = laundrybag_factory(clothes_list = [])
    assert laundrybag.label is None
    assert laundrybag.status is LaundryBagState.COLLECTING
    laundrybag.append(clothes_factory(label = LaundryLabel.WASH))

    assert laundrybag.label is LaundryLabel.WASH
