from config import APIConfigurations

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src import domain
from src.infrastructure.db.setup import get_uow
from src.infrastructure.api.routes.user_router import get_current_user


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
        db = TestingSessionLocal()
        yield db
    finally :
        db.close()

def override_get_session() :
    return TestingSessionLocal

def override_get_current_user() :
    userid = 'test'
    return domain.User(userid = userid, 
                       password = 'test-password',
                       phone_number = 'test-phone-num',
                       address = 'test-address'
                       )
    

def override_get_uow(session_factory : Session = Depends(override_get_session)) :
    return SqlAlchemyUnitOfWork(session_factory)

app.dependency_overrides[get_uow] = override_get_uow
app.dependency_overrides[get_current_user] = override_get_current_user

test_app = TestClient(app)  



route_path = f'/v{APIConfigurations.version}'
    


def test_list_user() :
    response = test_app.get(f'{route_path}/user/list')
    assert response.status_code == 200


def test_create_user() : 
    response = test_app.post(f'{route_path}/user/create',
                  json = {
                      'userid' : 'eunsung',
                      'address' : '서울시 송파구',
                      'password1' : 'test_password',
                      'password2' : 'test_password',
                      'phone_number' : 'test_phone_number'
                  }

                )
    assert response.status_code == 204

def test_fail_create_user() :
    response = test_app.post(f'{route_path}/user/create',
                  json = {
                      'userid' : 'eunsung',
                      'address' : '서울시 송파구',
                      'password1' : 'test_password',
                      'password2' : 'test_password123',
                      'phone_number' : 'test_phone_number'
                  }

                )
    assert response.status_code == 422, '패스워드가 서로 다름'

def test_request_order() : 
    userid = 'test'

    test_app.post(f'{route_path}/user/create', 
                  json = {
                      'userid' : userid,
                      'address' : '서울시 송파구',
                      'password1' : 'test_password',
                      'password2' : 'test_password',
                      'phone_number' : 'test_phone_number'
                  }
                  )

    response = test_app.post(
        f'{route_path}/user/{userid}/orders',
        json = 
                {
                'clothes_list' : [{
                    'clothesid' : 'sample_clothes',
                    'label' : '드라이클리닝',
                    'volume' : float(3.0)
                    }
                ]
            }    
    )

    assert response.status_code == 204
    
    
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