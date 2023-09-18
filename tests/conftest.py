from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src.infrastructure.api.app import app
from src.domain.base import Base

from fastapi.testclient import TestClient
from fastapi import FastAPI

import requests
from requests.exceptions import ConnectionError
import random

from typing import List, Dict, Optional 

from src.domain import Clothes, ClothesState, LaundryBag, LaundryBagState, LaundryLabel, Order, User, OrderState
import config

import time
from datetime import datetime
from tests.random_refs import random_clothesid, random_laundrybagid, random_orderid, random_userid

from pathlib import Path

import pytest

today = datetime.today()




@pytest.fixture
def clothes_factory() :
    def _clothes_factory(clothesid = None, label=None, volume=None, status = None, received_at = None):
        if clothesid is None :
            clothesid = random_clothesid()
        if label is None:
            label = random.choice([LaundryLabel.WASH, LaundryLabel.DRY, LaundryLabel.HAND])

        if volume is None:
            volume = float(random.randint(5, 15))
        if status is None:
            status = ClothesState.PREPARING # as preparing is a default state.
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
        return Clothes(clothesid=clothesid, label=label, volume=volume, status=status, received_at=received_at)
    yield _clothes_factory

@pytest.fixture
def laundrybag_factory() :
    def _laundrybag_factory(laundrybagid: str = None,
                            clothes_list: List[Clothes] = [], 
                            status : LaundryBagState = LaundryBagState.COLLECTING,
                            ):
        if laundrybagid is None : 
            laundrybagid = random_laundrybagid()
        laundrybag = LaundryBag(laundrybagid = laundrybagid, 
                                 status = status)
        for clothes in clothes_list :
            
            laundrybag.append(clothes)
        return laundrybag
    yield _laundrybag_factory



@pytest.fixture
def order_factory(clothes_factory) :
    def _order_factory(userid : str = None,
                       orderid: str = None, 
                       clothes_list: List[Clothes] = [clothes_factory(label=LaundryLabel.WASH, received_at = today)], 
                       received_at: Optional[datetime] = None) :
        if userid is None :
            userid = random_userid()
        if orderid is None :
            orderid = random_orderid()


        return Order(userid = userid, 
                            orderid = orderid, 
                            clothes_list = clothes_list, 
                            received_at = received_at)

    yield _order_factory


@pytest.fixture
def user_factory() :
    def _user_factory(userid: str = None, address: str = 'test-adress', orderlist : List = []) :
        if userid is None :
            userid = random_userid()
        return User(userid = userid, address = address, orderlist = orderlist)

    yield _user_factory


@pytest.fixture
def in_memory_db() :
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_db) :
    yield sessionmaker(bind = in_memory_db,  autoflush=False, autocommit = False)

@pytest.fixture
def session(session_factory) :
    return session_factory()

@pytest.fixture
def uow_factory(session_factory) :
    yield SqlAlchemyUnitOfWork(session_factory)

@pytest.fixture
def test_app() -> TestClient : 
    yield TestClient(app = app)
