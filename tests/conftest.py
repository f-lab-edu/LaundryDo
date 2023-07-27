from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src import dbmodel 

from src.infrastructure.db.sqlalchemy.orm import start_mappers
from src.infrastructure.db.sqlalchemy.setup import metadata

from src.dbmodel.base import Base

import requests
from requests.exceptions import ConnectionError
from uuid import uuid4
import random

from typing import List, Dict, Optional 

from src.domain import Clothes, ClothesState, LaundryBag, LaundryLabel, Order, User, OrderState
import config

import time
from datetime import datetime

from pathlib import Path

import pytest

today = datetime.today()


@pytest.fixture
def clothes_factory() :
    def _clothes_factory(clothesid = None, label=None, volume=None, status=None, received_at = None):
        if clothesid is None :
            clothesid = f'clothes-{str(uuid4())[:2]}'
        if label is None:
            label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

        if volume is None:
            volume = float(random.randint(5, 15))
        if status is None:
            status = random.choice(
                [
                    ClothesState.PREPARING,
                    ClothesState.CANCELLED,
                    ClothesState.DISTRIBUTED,
                    ClothesState.PROCESSING,
                    ClothesState.DONE,
                    ClothesState.RECLAIMED
                ]
            )
        return Clothes(clothesid=clothesid, label=label, volume=volume, status=status, received_at=received_at)
    yield _clothes_factory


@pytest.fixture
def dbmodel_clothes_factory() :
    def _dbmodel_clothes_factory(clothesid = None, label=None, volume=None, status=None, received_at = None):
        if clothesid is None :
            clothesid = f'clothes-{str(uuid4())[:2]}'
        if label is None:
            label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

        if volume is None:
            volume = float(random.randint(5, 15))
        # if status is None:
        #     status = random.choice(
        #         [
        #             ClothesState.PREPARING,
        #             ClothesState.CANCELLED,
        #             ClothesState.DISTRIBUTED,
        #             ClothesState.PROCESSING,
        #             ClothesState.DONE,
        #             ClothesState.RECLAIMED
        #         ]
        #     )
        return dbmodel.Clothes(clothesid=clothesid, label=label, volume=volume, status=status, received_at=received_at)
    yield _dbmodel_clothes_factory

@pytest.fixture
def dbmodel_laundrybag_factory(dbmodel_clothes_factory) :
    def _dbmodel_laundrybag_factory(laundrybagid: str = f'laundrybag-{str(uuid4())[:2]}-0',
                            clothes_list: List[Clothes] = [], 
                            created_at: datetime = today):
        return dbmodel.LaundryBag(laundrybagid = laundrybagid, clothes_list = clothes_list, created_at = created_at)

    yield _dbmodel_laundrybag_factory



@pytest.fixture
def dbmodel_order_factory(clothes_factory) :
    def _dbmodel_order_factory(userid : str = f'user-{str(uuid4())[:2]}',
                       orderid: str = f'order-{str(uuid4())[:2]}', 
                       clothes_list: List[Clothes] = [clothes_factory(label=LaundryLabel.WASH, received_at = today)], 
                       received_at: Optional[datetime] = None, 
                       status : OrderState = OrderState.SENDING
                    ) :
        return dbmodel.Order(userid = userid, orderid = orderid, clothes_list = clothes_list, received_at = received_at, status = status)

    yield _dbmodel_order_factory


@pytest.fixture
def dbmodel_user_factory() :
    def _dbmodel_user_factory(userid: str = f'user-{str(uuid4())[:2]}', address: str = 'test-adress', orderlist : List = []) :
        return dbmodel.User(userid = userid, address= address, orderlist = orderlist)

    yield _dbmodel_user_factory




@pytest.fixture
def user_factory() :
    def _user_factory(userid: str = f'user-{str(uuid4())[:2]}', address: str = 'test-adress', orderlist : List = []) :
        return User(userid = userid, address= address, orderlist = orderlist)

    yield _user_factory


@pytest.fixture
def order_factory(clothes_factory) :
    def _order_factory(userid : str = f'user-{str(uuid4())[:2]}',
                       orderid: str = f'order-{str(uuid4())[:2]}', 
                       clothes_list: List[Clothes] = [clothes_factory(label=LaundryLabel.WASH, received_at = today)], 
                       received_at: Optional[datetime] = None, 
                       status : OrderState = OrderState.SENDING
                    ) :
        return Order(userid = userid, orderid = orderid, clothes_list = clothes_list, received_at = received_at, status = status)

    yield _order_factory

@pytest.fixture
def laundrybag_factory(clothes_factory) :
    def _laundrybag_factory(laundrybagid: str = f'laundrybag-{str(uuid4())[:2]}-0',
                            clothes_list: List[Clothes] = [], 
                            created_at: datetime = today):
        return LaundryBag(laundrybagid = laundrybagid, clothes_list = clothes_list, created_at = created_at)

    yield _laundrybag_factory


@pytest.fixture
def in_memory_db() :
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_db) :
    start_mappers()
    yield sessionmaker(bind = in_memory_db,  autoflush=False, autocommit = False)
    clear_mappers()

@pytest.fixture
def session(session_factory) :
    return session_factory()

@pytest.fixture
def base_in_memory_db() :
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def base_session_factory(base_in_memory_db) :
    yield sessionmaker(bind = base_in_memory_db,  autoflush=False, autocommit = False)

@pytest.fixture
def base_session(base_session_factory) :
    return base_session_factory()

# def wait_for_webapp_to_come_up() :
#     deadline = time.time() + 10
#     url = config.get_api_url()
#     while time.time() < deadline :
#         try :
#             return requests.get(url)
#         except ConnectionError :
#             time.sleep(0.5)
#     pytest.fail('API never came up')


# @pytest.fixture
# def restart_api() :
#     ###
#     (Path(__file__).parent / 'app.py').touch()
#     time.sleep(0.5)
#     wait_for_webapp_to_come_up()