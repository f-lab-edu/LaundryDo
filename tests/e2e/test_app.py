import requests
import pytest

from config import APIConfigurations
from datetime import datetime, date

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool, NullPool
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src import domain
from src.domain.base import Base
from src.infrastructure.db.setup import get_db, get_session
from src.infrastructure.db.initialize import initialize_table
from src.infrastructure.api.app import app


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread' : False},
    poolclass = StaticPool
)

initialize_table(engine=engine, checkfirst = True)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def override_get_db() :
    try :
        db = TestingSessionLocal()
        yield db
    finally :
        db.close()

# def get_uow() :
#     return SqlAlchemyUnitOfWork(TestingSessionLocal)

def override_get_session() :
    return TestingSessionLocal



app.dependency_overrides[get_db] = override_get_db
test_app = TestClient(app)  

uow = SqlAlchemyUnitOfWork(TestingSessionLocal)


route_path = f'/v{APIConfigurations.version}'
    
def teardown_function() :
    pass

def test_ping() :
    response = test_app.get('/ping')

    assert response.json() == 'pong'    
    assert response.status_code == 200

def test_list_user() :
    response = test_app.get(f'{route_path}/user/list')
    assert response.status_code == 200


def test_create_user() : 
    response = test_app.post(f'{route_path}/user/create',
                  json = {
                      'userid' : 'eunsung1',
                      'address' : '서울시 송파구',
                  }

                )
    assert response.status_code == 204



def test_request_order() : 
    userid = 'tom'

    response = test_app.post(
        f'{route_path}/user/{userid}/orders',
        json = 
                {
                # 'userid' : userid,
                'clothes_list' : [{
                    'clothesid' : 'sample_clothes',
                    'label' : '드라이클리닝',
                    'volume' : float(3.0)
                    }
                ]
            }    
    )

    assert response.status_code == 200
    data = response.json()
    assert data['clothes_list'][0]['clothesid'] == 'sample_clothes'
    
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