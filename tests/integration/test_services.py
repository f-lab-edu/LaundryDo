from src.domain import LaundryLabel, LaundryBagState, LaundryBag, ClothesState, OrderState
from src.domain.spec import MACHINE_MAXVOLUME
from src.application import request_order, cancel_order

from src.application import services

from src.infrastructure.repository import FakeSession

from src.application.unit_of_work import SqlAlchemyUnitOfWork, MemoryUnitOfWork

from src.infrastructure.repository import MemoryOrderRepository, MemoryLaundryBagRepository
from src.infrastructure.repository import SqlAlchemyOrderRepository, SqlAlchemyLaundryBagRepository

from collections import deque

import pytest
from datetime import datetime
from uuid import uuid4

today = datetime.today()



def test_order_allocated_to_new_laundrybag(uow_factory, order_factory, laundrybag_factory, clothes_factory) :
    # register orders  
    order = order_factory(clothes_list = [clothes_factory(label = LaundryLabel.WASH, volume = MACHINE_MAXVOLUME)])
    with uow_factory :
        uow_factory.orders.add(order)
        uow_factory.commit()
    # there is no laundrybag in wait
    
    # allocate clothes into laundrybag
    services.allocate_clothes_in_laundrybag(uow_factory)

    with uow_factory :
        assert len(uow_factory.laundrybags.list()) == 1


