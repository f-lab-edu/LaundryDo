from src.domain import Order
from enum import Enum

from typing import List, Dict, Annotated
from datetime import datetime

from fastapi import FastAPI, Query, Body, Depends
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from src import domain 
from src.infrastructure.fastapi import schemas
from src.application import services

import databases
from src.infrastructure.db.sqlalchemy.setup import engine, session, SQLALCHEMY_DATABASE_URL
from src.domain.base import Base

import config

from apscheduler.schedulers.background import BackgroundScheduler

from src.application.unit_of_work import SqlAlchemyUnitOfWork

app = FastAPI()



# dependency
MEMORY_SESSION = 'sqlite:///:memory:'
# database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(MEMORY_SESSION, echo = True)
Base.metadata.create_all(bind = engine)

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)


uow = SqlAlchemyUnitOfWork(session)
# laundry_service = LaundryService(session = database,
#                                  order_repository = SqlAlchemyOrderRepository,
#                                  laundrybag_repository = SqlAlchemyLaundryBagRepository,
#                                  clothes_repository = SqlAlchemyClothesRepository,
#                                  machine_repository = SqlAlchemyMachineRepository)

### scenario
with uow :

    user1 = domain.User(userid = 'Bob', address = '서울시 강남구')
    user2 = domain.User(userid = 'Jason', address = '서울시 노원구')

    order1 = domain.Order(
                    userid = 'Bob',
                    orderid = 'Bob_order1',
                    clothes_list = [domain.Clothes(
                                        clothesid='흰티셔츠',
                                        label = domain.LaundryLabel.DRY,
                                        volume = 3,
                                    ),
                                    domain.Clothes(
                                        clothesid='청바지',
                                        label = domain.LaundryLabel.HAND,
                                        volume = 6,
                                    ),
                                ],
                    received_at = datetime.now()
                        )
    order2 = domain.Order(
                    userid = 'Jason',
                    orderid = 'Jason_order5',
                    clothes_list = [domain.Clothes(
                                        clothesid='갈색 면바지',
                                        label = domain.LaundryLabel.WASH,
                                        volume = 4,
                                    ),
                                    domain.Clothes(
                                        clothesid='초록색 블라우스',
                                        label = domain.LaundryLabel.DRY,
                                        volume = 2,
                                    ),
                                ],
                    received_at = datetime.now())
    user1.orderlist.append(order1)
    user2.orderlist.append(order2)

    uow.users.add(user1)
    uow.users.add(user2)
    uow.commit()

    for i in range(10) :
        machine = domain.Machine(machineid = f'machine_{i}')
        uow.machines.add(machine)
    

def get_db() :
    try :
        yield session
    finally :
        session.close()


# def print_hi() :
#     print('hi')

@app.on_event('startup')
def init_monitor():#session : Session = Depends(get_db)) :
    ## listening on db
    # uow = SqlAlchemyUnitOfWork(session)
    scheduler = BackgroundScheduler()

    scheduler.add_job(services.change_laundrybagstate_if_time_passed, 'cron', second = '*/10', args = [uow] )
    # scheduler.add_job(services.put_laundrybag_into_machine, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.reclaim_clothes_from_machine, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.update_orderstate_fully_reclaimed, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.ship, 'cron', second='*/10', args =[uow] )
    scheduler.start()


# def print_hi() :
#     print('hi')

# @app.on_event('startup')
# def init_monitor() :
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(print_hi, 'cron', second = '*/5')
#     scheduler.start()


# @app.on_event('startup')
# async def startup() :
#     await database.connect()

# @app.on_event('shutdown')
# async def shutdown() :
#     await database.disconnect()


@app.get('/')
async def root() :
    return {'LaundryDo' : 'Welcome'}

@app.get('/users/{userid}', response_model = schemas.Order)
async def request_orderlist(userid : str, session : Session = Depends(get_db)) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        return uow.orders.get_by_userid(userid=userid)


@app.get('/users/{userid}/orders/{orderid}')
async def request_order_info(userid : str, orderid : str, session : Session = Depends(get_db)) -> schemas.Order : ## TODO : orders only be accessible for one user.
    '''
    request estimate time for order in process. if order is done or cancelled, return 0.
    '''
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        return uow.orders.get_by_orderid(orderid = orderid)


@app.post('/users/{userid}/orders', response_model = schemas.Order)
async def request_order(userid : str, order : Annotated[ schemas.Order, 
            Body(
                examples = [
                    {   
                        'userid' : '[userid]',
                        "orderid" : '[userid]-order-[num]',
                        "description" : "세탁 요청한 옷들의 리스트가 담긴 주문 정보",
                        'clothes_list' : [{
                            "clothesid" : "흰티셔츠",
                            "label" : "드라이클리닝",
                            "volume" : 3,
                                }
                            ],
                        "received_at" : datetime(2023, 7, 21, 10, 11),
                    }
                ]
            )
        ], 
        session : Session = Depends(get_db)
    ) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        services.request_order(uow,**dict(order))
        uow.commit()

    return order


@app.put('/users/{userid}/orders/{orderid}')
async def cancel_order(userid : str, orderid : str, session : Session = Depends(get_db)) :#-> schemas.Order :
    uow = SqlAlchemyUnitOfWork(session)
    
    with uow :
        order = services.cancel_order(uow, userid, orderid)
        order = schemas.Order.model_validate(order)
        order.commit()

    return order















# class Order(BaseModel) :
#     userid : str
#     clothes_list : list | None = None



# orders = {'eunsung' : {
#         'order_list' : [
#             {'orderid' : 1,
#             'clothes' : [{'clothesid' : 1, 'label' : 'wash'},],
#             },
#             ]
#         },
#     }

# class Ordertype(str, Enum) :
#     REQUEST = 'request'
#     CANCEL = 'cancel'

# @app.get("/")
# def root():
#     return {"message": "welcome to LaundryDo"}



# # @app.delete('/orders/{orderid}')
# # def cancel_order(orderid : int) :
# #     pass


# # @app.get("/orders")
# # def check_order_history(order):
# #     return order


# # @app.get("/orders/{orderid}/")
# # def request_estimate_time(orderid: int):
# #     return orders[orderid]

# @app.get('/ordertype/{ordertype}') 
# def request_type(ordertype : Ordertype) :
#     if ordertype is Ordertype.REQUEST :
#         return ordertype
#     else :
#         print(ordertype)

# @app.get("/files/{file_path:path}")
# def read_file(file_path : str) :
#     with open(file_path, 'r') as f :
#         file = f.readlines()
    
#     return file

# @app.post('/db/orders')
# async def register_order(order : Order) :
#     query = orders.select()
#     return await database.fetch_all(query)



# @app.get('/users/')
# def request_userid(userid : Annotated[str | None, Query(max_length = 50 )]) :
#     return orders[userid]

