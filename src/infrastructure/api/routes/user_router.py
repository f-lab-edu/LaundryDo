from fastapi import APIRouter, Body, Depends
from starlette import status

from datetime import datetime
from typing import List, Annotated
from src.infrastructure.api import schemas
from src.infrastructure.db.setup import session, get_db, get_session
from src import domain
from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from sqlalchemy.orm import Session

from src.infrastructure.repository import (
    SqlAlchemyUserRepository,
    SqlAlchemyOrderRepository,
)


router = APIRouter()


@router.get('/list', response_model = List[schemas.User])
def list_user(db : Session = Depends(get_db)) :
    user_repo = SqlAlchemyUserRepository(db)
    all_users = user_repo.list()
    all_users = [schemas.User.model_validate(user) for user in all_users]
    return all_users
    
    


@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create : schemas.User, db : Session = Depends(get_db)) :
    user_repo = SqlAlchemyUserRepository(db)
    
    user = domain.User(userid = _user_create.userid,
                        address = _user_create.address)
    user_repo.add(user)
    db.commit()

    return _user_create
    


@router.get('/{userid}/orders', response_model = List[schemas.Order])
def request_orderlist(userid : str, db : Session = Depends(get_db)) :
    order_repo = SqlAlchemyOrderRepository(db)

    orders = order_repo.get_by_userid(userid = userid)
    return orders


@router.post('/{userid}/orders', response_model = schemas.OrderCreate)
def request_order(userid : str, order : schemas.OrderCreate, db : Session = Depends(get_db)) :
                    # Body(
                    #     examples = [
                    #         {   
                    #         # "description" : "세탁 요청한 옷들의 리스트가 담긴 주문 정보",
                    #         'clothes_list' : [{
                    #                     "clothesid" : "흰티셔츠",
                    #                     "label" : "드라이클리닝",
                    #                     "volume" : 3,
                    #                 }],
                    #         }
                    #     ])
                    # ]         
                
    # TODO if userid not found, raise Error
    order_repo = SqlAlchemyOrderRepository(db)
    
    new_order = domain.Order(orderid = f'orderid-{userid}',
                             userid = userid,
                             clothes_list = [domain.Clothes(**dict(clothes)) for clothes in order.clothes_list],
                             received_at = datetime.now()
                             )

    
    order_repo.add(new_order)
    db.commit()
    
    return new_order