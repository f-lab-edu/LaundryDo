from src.domain import Order
from enum import Enum

from typing import List, Dict, Annotated
from datetime import datetime

from fastapi import FastAPI, Query, Body, Depends

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

from src.infrastructure.fastapi.routes import user_router, order_router


app = FastAPI()

app.include_router(user_router.router)
app.include_router(order_router.router)


uow = SqlAlchemyUnitOfWork(session)

## TODO 테스트 샘플 넣는 더 나은 방법? 현재는 docker-compose down 후에 up해야함
## db에 값이 들어가서 테스트 중복 발생
### scenario
# with uow :

#     user1 = domain.User(userid = 'Bob', address = '서울시 강남구')
#     user2 = domain.User(userid = 'Jason', address = '서울시 노원구')

#     order1 = domain.Order(
#                     userid = 'Bob',
#                     orderid = 'Bob_order1',
#                     clothes_list = [domain.Clothes(
#                                         clothesid='흰티셔츠',
#                                         label = domain.LaundryLabel.DRY,
#                                         volume = 3,
#                                     ),
#                                     domain.Clothes(
#                                         clothesid='청바지',
#                                         label = domain.LaundryLabel.HAND,
#                                         volume = 6,
#                                     ),
#                                 ],
#                     received_at = datetime.now()
#                         )
#     order2 = domain.Order(
#                     userid = 'Jason',
#                     orderid = 'Jason_order5',
#                     clothes_list = [domain.Clothes(
#                                         clothesid='갈색 면바지',
#                                         label = domain.LaundryLabel.WASH,
#                                         volume = 4,
#                                     ),
#                                     domain.Clothes(
#                                         clothesid='초록색 블라우스',
#                                         label = domain.LaundryLabel.DRY,
#                                         volume = 2,
#                                     ),
#                                 ],
#                     received_at = datetime.now())
#     user1.orderlist.append(order1)
#     user2.orderlist.append(order2)

#     uow.users.add(user1)
#     uow.users.add(user2)
#     uow.commit()

#     for i in range(10) :
#         machine = domain.Machine(machineid = f'machine_{i}')
#         uow.machines.add(machine)
    
@app.on_event('startup')
def init_monitor():#session : Session = Depends(get_db)) :
    ## listening on db
    # uow = SqlAlchemyUnitOfWork(session)
    scheduler = BackgroundScheduler()

    ## TODO apscheduler job에 대한 session이 중복되어 생기는 문제

    scheduler.add_job(services.change_laundrybagstate_if_time_passed, 'cron', second = '*/10', args = [uow] )
    # scheduler.add_job(services.put_laundrybag_into_machine, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.reclaim_clothes_from_machine, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.update_orderstate_fully_reclaimed, 'cron', second='*/10', args =[uow] )
    # scheduler.add_job(services.ship, 'cron', second='*/10', args =[uow] )
    scheduler.start()

@app.on_event('shutdown')
def shutdown() :
    pass

@app.get('/ping')
def ping() :
    return 'pong'

@app.get('/')
async def root() :
    return {'LaundryDo' : 'Welcome'}


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

