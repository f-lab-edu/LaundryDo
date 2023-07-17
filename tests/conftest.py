from uuid import uuid4
import random

from typing import List, Dict

from src.domain.model import Clothes, ClothesState, LaundryBag, LaundryLabel, Order, User, OrderState
from datetime import datetime
import pytest

time_now = datetime(2023, 7, 12, 20, 48, 13)

@pytest.fixture
def clothes_factory() :
    def _clothes_factory(label=None, volume=None, status=None, received_at = None):

        id = str(uuid4())[:4]
        if label is None:
            label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

        if volume is None:
            volume = random.randint(5, 15)
        if status is None:
            status = random.choice(
                [
                    ClothesState.PREPARING,
                    ClothesState.CANCELLED,
                    ClothesState.DISTRIBUTED,
                    ClothesState.PROCESSING,
                    ClothesState.DONE,
                ]
            )
        return Clothes(id=id, label=label, volume=volume, status=status, received_at=received_at)
    yield _clothes_factory


@pytest.fixture
def user_factory() :
    def _user_factory(id: str = 'test-username', address: str = 'test-adress', orderlist : List = []) :
        return User(id = id, address= address, orderlist = orderlist)

    yield _user_factory


@pytest.fixture
def order_factory(clothes_factory) :
    def _order_factory(id: str = 'test-order', 
                       clothes_list: List = [clothes_factory(received_at = time_now)], 
                       received_at: datetime = None, 
                       status : OrderState = OrderState.SENDING
                    ) :
        return Order(id, clothes_list, received_at, status)

    yield _order_factory

@pytest.fixture
def laundrybag_factory(clothes_factory) :
    def _laundrybag_factory(clothes_list: List[Clothes] = [clothes_factory()], 
                            createdTime: datetime = time_now):
        return LaundryBag(clothes_list, createdTime)

    yield _laundrybag_factory



@pytest.fixture
def new_user():
    user1 = User(id="eunsung", address="서울시 송파구", orderlist=[])
    return user1


@pytest.fixture
def new_order():
    order = Order(
        "order1", received_at=time_now, clothes_list=[new_clothes() for _ in range(10)]
    )

    return order
