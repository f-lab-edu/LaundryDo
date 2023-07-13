from uuid import uuid4
import random

from model import Clothes, LaundryLabel, Order, User
from datetime import datetime
import pytest

time_now = datetime(2023, 7, 12, 20, 48, 13)


def new_clothes() :
    clothesid = str(uuid4())[:4]
    label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])
    volume = random.random()
    status = random.choice([ClothesState.PREPARING, ClothesState.CANCELLED, ClothesState.DIVIDED, ClothesState.PROCESSING, ClothesState.DONE])

    return Clothes(clothesid, label, volume, status)

@pytest.fixture
def new_user() :
    user1 = User(id = 'eunsung', address = '서울시 송파구', orderlist = [])
    return user1

@pytest.fixture
def new_order() :
    clothes1 = Clothes('blue top', LaundryLabel.DRY, 0.2)
    clothes2 = Clothes('black jeans', LaundryLabel.WASH, 0.3)
    order = Order('order1', received_at = time_now, clothesBag = [clothes1, clothes2])

    return order

