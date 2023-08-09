import requests
import pytest
import config
from datetime import datetime, date

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src.domain.base import Base
from src.infrastructure.fastapi.app import app, get_db


SQLALCHEMY_DATABASE_URL = 'sqlite://'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread' : False},
    poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)
Base.metadata.create_all(bind = engine)

def override_get_db() :
    try :
        yield TestingSessionLocal
    finally :
        print('is db down?')
    # finally :
    #     db.close()

app.dependency_overrides[get_db] = override_get_db
test_app = TestClient(app)

uow = SqlAlchemyUnitOfWork(TestingSessionLocal)


def test_api_connection() :
    response = test_app.get('/')
    assert response.status_code == 200



def test_request_order() : 

    userid = 'tom'
    orderid = 'tom-test230809-1'


    response = test_app.post(
        f'/users/{userid}/orders',
        json = {
                'orderid' : orderid,
                'userid' : userid,
                'clothes_list' : [
                    {
                        'clothesid' : 'sample-clothes1',
                        'label' : '드라이클리닝',
                        'volume' : 3,
                    }
                ],
                'received_at' : '2023-08-09',
        }    
    )

    assert response.status_code == 200, response.text
    data = response.json()

    
    # # put order in db
    # order1 = order_factory()
    # order1.request_order(clothes_list = [clothes_factory() for _ in range(5)])
    # session.add(order1)
    # session.commit()


    pass

def test_cancel_order() :
    pass


def test_request_order_progress() :
    pass