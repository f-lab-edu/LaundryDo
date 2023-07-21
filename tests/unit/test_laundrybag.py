from src.domain import distribute_order, put_in_laundrybag, ClothesState, LaundryLabel
from src.domain.laundrybag import LaundryBagState
from src.infrastructure.db.memory.repository import MemoryOrderRepository, MemoryLaundryBagRepository
from src.infrastructure.db.sqlalchemy.repository import SqlAlchemyOrderRepository, SqlAlchemyLaundryBagRepository

from datetime import datetime, timedelta

from tests.conftest import clothes_factory, laundrybag_factory


today = datetime.today()
yesterday = today - timedelta(days=1)
longtimeago = today - timedelta(days=10)

def test_laundrybag_clothes_status_changed_to_distributed(laundrybag_factory, clothes_factory):
    laundryBag = laundrybag_factory(clothes_list = [clothes_factory() for _ in range(10)])

    assert all([clothes.status == ClothesState.DISTRIBUTED for clothes in laundryBag])


########TODO
def test_laundrybags_with_same_laundryLabel_combine_into_same_laundrybag(session, order_factory, laundrybag_factory, clothes_factory):
    order_repo = SqlAlchemyOrderRepository(session)
        
    order_repo.add(order_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 5)]))
                    
                    
    
    laundrybag_repo = SqlAlchemyLaundryBagRepository(session)
    laundrybag_repo.add(laundrybag_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = 20)]))

    laundrylabeldict = distribute_order(order_repo)
    put_in_laundrybag(laundrybag_repo, laundrylabeldict)
    laundrybags_in_ready = laundrybag_repo.get_by_status(status = LaundryBagState.READY)

    assert len(laundrybag_repo.list()) == 2

def test_laundrybags_sorted_by_time(laundrybag_factory):
    longtimeago_laundryBag = laundrybag_factory(created_at= longtimeago)
    yesterday_laundryBag = laundrybag_factory(created_at= yesterday)
    today_laundryBag = laundrybag_factory(created_at= today)

    assert sorted([today_laundryBag, yesterday_laundryBag, longtimeago_laundryBag]) \
                == [longtimeago_laundryBag, yesterday_laundryBag, today_laundryBag,]

