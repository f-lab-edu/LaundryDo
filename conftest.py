from uuid import uuid4
import random

from model import Clothes, ClothesState, LaundryLabel, Order, User
from datetime import datetime
import pytest

time_now = datetime(2023, 7, 12, 20, 48, 13)

@pytest.fixture
def new_clothes() :
    ## TODO : they are not really random. random fixed.
    clothesid = str(uuid4())[:4]
    label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])
    volume = random.random()
    status = random.choice([ClothesState.PREPARING, ClothesState.CANCELLED, ClothesState.DIVIDED, ClothesState.PROCESSING, ClothesState.DONE])

    return Clothes(clothesid = clothesid, label = label, volume = volume, status = status)

@pytest.fixture
def new_user() :
    user1 = User(id = 'eunsung', address = '서울시 송파구', orderlist = [])
    return user1

@pytest.fixture
def new_order(new_clothes) :
    
    order = Order('order1', received_at = time_now, clothes_list = [new_clothes for _ in range(10)])

    return order

