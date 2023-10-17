from logging import getLogger
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

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from contextlib import contextmanager, asynccontextmanager

from src.domain.clothes import LaundryLabel
from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.api.routes import user_router, order_router
from src.infrastructure.db import initialize


logger = getLogger(__name__)
# initailize datbase tables
# initialize.initialize_table(engine = engine, checkfirst = True)





app = FastAPI(
    title = APIConfigurations.title,
    description = APIConfigurations.description,
    version = APIConfigurations.version,
    # lifespan = monitoring_job
)

app.include_router(user_router.router, prefix = f'/v{APIConfigurations.version}/user')
app.include_router(order_router.router, prefix = f'/v{APIConfigurations.version}/order')


uow = SqlAlchemyUnitOfWork(session)

@app.on_event('startup')
def monitoring_job() :
    # monitoring job

    executors = {
        'default' : ThreadPoolExecutor(1)
    }

    scheduler = BackgroundScheduler(executors = executors)

    ## TODO apscheduler job에 대한 session이 중복되어 생기는 문제

    scheduler.add_job(services.update_laundrybag_state, 'cron', second = '*/10', args = [uow])
    scheduler.add_job(services.allocate_laundrybag_to_machine, 'cron', second='*/10', args =[uow])
    scheduler.add_job(services.update_machine_state_if_laundry_done, 'cron', second='*/10', args =[uow] )
    scheduler.add_job(services.reclaim_clothes_from_machine, 'cron', second='*/10', args =[uow] )
    scheduler.add_job(services.ship_finished_order, 'cron', second='*/10', args =[uow] )
    scheduler.start()

    return

@app.get('/ping')
def ping() :
    return 'pong'

@app.get('/')
async def root() :
    return {'LaundryDo' : 'Welcome'}
