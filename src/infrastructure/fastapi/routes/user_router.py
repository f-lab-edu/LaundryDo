from fastapi import APIRouter, Body, Depends
from starlette import status

from datetime import datetime
from typing import List, Annotated
from src.infrastructure.fastapi import schemas
from src.infrastructure.db.sqlalchemy.setup import session
from src import domain
from src.application.unit_of_work import SqlAlchemyUnitOfWork, get_uow
from src.application import services
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = '/user'
)


@router.get('/list', response_model = List[schemas.User])
def list_user() :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        all_users = uow.users.list()
        all_users = [schemas.User.model_validate(user) for user in all_users]
        return all_users
    
    


@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create : schemas.User) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        user = domain.User(userid = _user_create.userid,
                            address = _user_create.address)
        uow.users.add(user)
        uow.commit()

    return _user_create
    



@router.get('/{userid}/orders', response_model = List[schemas.Order])
def request_orderlist(userid : str) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        orders = uow.orders.get_by_userid(userid=userid)
    return orders


@router.post('/{userid}/order', status_code = status.HTTP_204_NO_CONTENT)
def request_order(userid : str, _order : Annotated[ schemas.OrderCreate, 
                    Body(
                        examples = [
                            {   
                            "description" : "세탁 요청한 옷들의 리스트가 담긴 주문 정보",
                            'clothes_list' : [{
                                        "clothesid" : "흰티셔츠",
                                        "label" : "드라이클리닝",
                                        "volume" : 3,
                                    }
                                ],
                            }
                        ])
                    ]         
                ) :
    uow = SqlAlchemyUnitOfWork(session)
    services.request_order(uow,
                            userid = userid,
                            clothes_list = _order.clothes_list,
                            received_at = datetime.now()
                            )