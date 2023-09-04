import requests
import pytest

from config import APIConfigurations
from datetime import datetime, date

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src import domain
from src.domain.base import Base
from src.infrastructure.db.setup import get_db
from src.infrastructure.db.initialize import initialize_table
from src.infrastructure.api.app import app


SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread' : False},
    poolclass = StaticPool
)

initialize_table(engine=engine, checkfirst = True)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def override_get_db() :
    try :
        db = TestingSessionLocal
        yield db
    finally :
        db.close()

def get_uow() :
    return SqlAlchemyUnitOfWork(TestingSessionLocal)

def override_get_uow() :
    try :
        db = TestingSessionLocal
        yield SqlAlchemyUnitOfWork(db)
    finally :
        db.close()



app.dependency_overrides[get_uow] = override_get_uow
test_app = TestClient(app)  

uow = SqlAlchemyUnitOfWork(TestingSessionLocal)


route_path = f'/v{APIConfigurations.version}'
    
def teardown_function() :
    pass

def test_ping() :
    response = test_app.get('/ping')

    assert response.json() == 'pong'    
    assert response.status_code == 200

from fastapi import Depends

def test_create_user() : 
    response = test_app.post(f'{route_path}/user/create',
                  json = {
                      'userid' : 'eunsung',
                      'address' : '서울시 송파구',
                  }

                  )
    assert response.status_code == 204
    

def test_request_order() : 
    userid = 'tom'
    orderid = 'tom-test230809-1'


    response = test_app.post(
        f'{route_path}/user/{userid}/orders',
        json = {
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

    assert response.status_code == 204
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






# def setup_function() :
    # # test_app.post('/request')


    # # user1 = domain.User(userid = 'Bob', address = '서울시 강남구')
    # # user2 = domain.User(userid = 'Jason', address = '서울시 노원구')

    # # order1 = domain.Order(
    # #                 userid = 'Bob',
    # #                 orderid = 'Bob_order1',
    # #                 clothes_list = [domain.Clothes(
    # #                                     clothesid='흰티셔츠',
    # #                                     label = domain.LaundryLabel.DRY,
    # #                                     volume = 3,
    # #                                 ),
    # #                                 domain.Clothes(
    # #                                     clothesid='청바지',
    # #                                     label = domain.LaundryLabel.HAND,
    # #                                     volume = 6,
    # #                                 ),
    # #                             ],
    # #                 received_at = datetime.now()
    # #                     )
    # # order2 = domain.Order(
    # #                 userid = 'Jason',
    # #                 orderid = 'Jason_order5',
    # #                 clothes_list = [domain.Clothes(
    # #                                     clothesid='갈색 면바지',
    # #                                     label = domain.LaundryLabel.WASH,
    # #                                     volume = 4,
    # #                                 ),
    # #                                 domain.Clothes(
    # #                                     clothesid='초록색 블라우스',
    # #                                     label = domain.LaundryLabel.DRY,
    # #                                     volume = 2,
    # #                                 ),
    # #                             ],
    # #                 received_at = datetime.now())
    # # user1.orderlist.append(order1)
    # # user2.orderlist.append(order2)

    # # uow.users.add(user1)
    # # uow.users.add(user2)
    # # uow.commit()

    # for i in range(10) :
    #     machine = domain.Machine(machineid = f'machine_{i}')
    #     uow.machines.add(machine)