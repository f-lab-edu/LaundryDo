###########
# Clothes #
###########

from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)


def test_sort_clothes_by_time(dbmodel_clothes_factory):
    clothes_today = dbmodel_clothes_factory(received_at = today)
    clothes_yesterday = dbmodel_clothes_factory(received_at = yesterday)
    clothes_longtimeago = dbmodel_clothes_factory(received_at = longtimeago)

    assert sorted([clothes_yesterday, clothes_longtimeago, clothes_today]) \
                == [clothes_longtimeago, clothes_yesterday, clothes_today]

