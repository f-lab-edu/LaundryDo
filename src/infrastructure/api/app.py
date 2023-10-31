from logging import getLogger
from src.domain import Order
from enum import Enum

from typing import List, Dict, Annotated
from datetime import datetime
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError


from src import domain 
from src.infrastructure.api import schemas
from src.infrastructure.api.crud import background_crud

from src.infrastructure.db.setup import engine, session, SQLALCHEMY_DATABASE_URL, get_uow

from config import APIConfigurations

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import contextmanager, asynccontextmanager

from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.api.routes import user_router, order_router
from src.infrastructure.api.crud import user_crud
from src.infrastructure.api.auth import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

logger = getLogger(__name__)
# initailize datbase tables
# initialize.initialize_table(engine = engine, checkfirst = True)





app = FastAPI(
    title = APIConfigurations.title,
    description = APIConfigurations.description,
    version = APIConfigurations.version,
    # lifespan = monitoring_job
)

app.include_router(user_router.router, prefix = f'/v{APIConfigurations.version}/users')
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

    scheduler.add_job(background_crud.update_laundrybag_state, 'cron', second = '*/10', args = [uow])
    scheduler.add_job(background_crud.allocate_laundrybag_to_machine, 'cron', second='*/10', args =[uow])
    scheduler.add_job(background_crud.update_machine_state_if_laundry_done, 'cron', second='*/10', args =[uow] )
    scheduler.add_job(background_crud.reclaim_clothes_from_machine, 'cron', second='*/10', args =[uow] )
    scheduler.add_job(background_crud.ship_finished_order, 'cron', second='*/10', args =[uow] )
    scheduler.start()

    return

@app.get('/ping')
def ping() :
    return 'pong'

@app.get('/')
async def root() :
    return {'LaundryDo' : 'Welcome'}



@app.post("/login")
def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(),
                           uow : SqlAlchemyUnitOfWork = Depends(get_uow)
                           ) -> schemas.Token :
    
    # check user and password
    user = user_crud.get_user(uow, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password) :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect userid or password",
            headers = {"WWW-Authenticate" : "Bearer"},
        )
    
    # make access token
    data = {
        "sub" : user.userid,
        "exp" : datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)

    return {
        "access_token" : access_token,
        "token_type" : "bearer",
        "userid" : user.userid
    }
    