from uuid import uuid4
import random

from model import Clothes, ClothesState, LaundryBag, LaundryLabel, Order, User
from datetime import datetime
import pytest

time_now = datetime(2023, 7, 12, 20, 48, 13)

def new_clothes(label = None, volume = None, status = None) :

    id = str(uuid4())[:4]
    if label is None :
        label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

    if volume is None : 
        volume = random.randint(5, 15)
    if status is None :
        status = random.choice([ClothesState.PREPARING, ClothesState.CANCELLED, ClothesState.DIVIDED, ClothesState.PROCESSING, ClothesState.DONE])
    return Clothes(id = id, label = label, volume = volume, status = status)
            


@pytest.fixture
def new_user() :
    user1 = User(id = 'eunsung', address = '서울시 송파구', orderlist = [])
    return user1

@pytest.fixture
def new_order() :
    order = Order('order1', received_at = time_now, clothes_list = [new_clothes() for _ in range(10)])

    return order

