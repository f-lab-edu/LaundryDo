from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from uuid import uuid4
from datetime import datetime
from typing import List, Annotated
from src.infrastructure.api import schemas
from src.infrastructure.db.setup import session, get_db, get_session
from src import domain


from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from src.infrastructure.api.crud import user_crud

from sqlalchemy.orm import Session

from src.infrastructure.repository import (
    SqlAlchemyUserRepository,
    SqlAlchemyOrderRepository,
)

from logging import getLogger

logger = getLogger(__name__)

router = APIRouter()


@router.get('/list', response_model = List[schemas.User])
def list_user(db : Session = Depends(get_db)) :
    user_repo = SqlAlchemyUserRepository(db)
    all_users = user_repo.list()
    all_users = [schemas.User.model_validate(user) for user in all_users]
    return all_users
    
    


@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create : schemas.UserCreate, db : Session = Depends(get_db)) :
    user = user_crud.get_existing_user(db, user_create = _user_create)
    if user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail = "이미 존재하는 사용자입니다.")

    user_crud.create_user(db, _user_create)



@router.get('/{userid}/orders', response_model = List[schemas.Order])
def request_orderlist(userid : str, db : Session = Depends(get_db)) :
    order_repo = SqlAlchemyOrderRepository(db)

    orders = order_repo.get_by_userid(userid = userid)
    return orders


@router.post('/{userid}/orders', status_code = status.HTTP_204_NO_CONTENT)
def request_order(userid : int, order : schemas.OrderCreate, db : Session = Depends(get_db)) :
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

    new_order = domain.Order(orderid = f'orderid-{userid}-{str(uuid4())[:4]}',
                             userid = userid,
                             clothes_list = [domain.Clothes(clothesid = clothes.clothesid,
                                                            label = clothes.label,
                                                            volume = clothes.volume,
                                                                   ) for clothes in order.clothes_list],
                             received_at = datetime.now()
                             )

    
    order_repo.add(new_order)
    db.commit()
    