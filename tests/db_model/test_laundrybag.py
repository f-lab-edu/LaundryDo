from src.dbmodel import ClothesState, LaundryLabel, LaundryBagState
from datetime import datetime, timedelta



today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)

def test_laundrybag_clothes_status_changed_to_distributed(dbmodel_laundrybag_factory, dbmodel_clothes_factory):
    laundryBag = dbmodel_laundrybag_factory(clothes_list = [dbmodel_clothes_factory() for _ in range(10)])

    assert laundryBag.clothes_list[0].status == ClothesState.DISTRIBUTED
    assert all([clothes.status == ClothesState.DISTRIBUTED for clothes in laundryBag.clothes_list])


def test_laundrybags_sorted_by_time(dbmodel_laundrybag_factory):
    longtimeago_laundryBag = dbmodel_laundrybag_factory(created_at= longtimeago)
    yesterday_laundryBag = dbmodel_laundrybag_factory(created_at= yesterday)
    today_laundryBag = dbmodel_laundrybag_factory(created_at= today)

    assert sorted([today_laundryBag, yesterday_laundryBag, longtimeago_laundryBag]) \
                == [longtimeago_laundryBag, yesterday_laundryBag, today_laundryBag,]

def test_laundrybag_label_changed_as_clothes_comes_in(dbmodel_laundrybag_factory, dbmodel_clothes_factory) :

    laundrybag = dbmodel_laundrybag_factory(clothes_list = [])
    assert laundrybag.label is None
    assert laundrybag.status is LaundryBagState.COLLECTING
    laundrybag.append(dbmodel_clothes_factory(label = LaundryLabel.WASH))

    assert laundrybag.label is LaundryLabel.WASH