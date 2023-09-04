from src.domain import Order
from enum import Enum

from typing import List, Dict, Annotated
from datetime import datetime

from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker, scoped_session, Session

from src import domain 
from src.infrastructure.api import schemas
from src.application import services

from src.infrastructure.db.setup import engine, session, SQLALCHEMY_DATABASE_URL

from config import APIConfigurations

from apscheduler.schedulers.background import BackgroundScheduler

from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.api.routes import user_router, order_router
from src.infrastructure.db.setup import engine
from src.infrastructure.db import initialize

# initailize datbase tables
initialize.initialize_table(engine = engine, checkfirst = True)

app = FastAPI(
    title = APIConfigurations.title,
    description = APIConfigurations.description,
    version = APIConfigurations.version
)

app.include_router(user_router.router, prefix = f'/v{APIConfigurations.version}/user')
app.include_router(order_router.router, prefix = f'/v{APIConfigurations.version}/order')


uow = SqlAlchemyUnitOfWork(session)

    
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
