from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from typing import List
from src.infrastructure.api import schemas

from src.infrastructure.db.setup import get_uow
from src import domain



from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from src.infrastructure.api.crud import user_crud, order_crud
from src.infrastructure.api.auth import oauth2_scheme, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session



from logging import getLogger

logger = getLogger(__name__)





router = APIRouter()



@router.get('/')
def list_user(uow : SqlAlchemyUnitOfWork = Depends(get_uow)) -> List[schemas.User] :
    with uow :
        all_users = uow.users.list()
        all_users = [schemas.User.model_validate(user) for user in all_users]
    return all_users
    
    
    


@router.post('/', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create : schemas.UserCreate, uow : SqlAlchemyUnitOfWork = Depends(get_uow)) :
    user = user_crud.get_existing_user(uow, user_create = _user_create)
    if user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail = "이미 존재하는 사용자입니다.")

    user_crud.create_user(uow, _user_create)



def get_current_user(token : str = Depends(oauth2_scheme),
                     uow : Session = Depends(get_uow)
                     ) -> schemas.User :
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"},
    )
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        userid = str = payload.get('sub')
        if userid is None :
            raise credentials_exception
    except JWTError :
        raise credentials_exception
    else :
        user = user_crud.get_user(uow, userid = userid)
        if user is None :
            raise credentials_exception
        return user


@router.get('/{userid}/orders')
def request_orderlist(userid : str, 
                      uow : Session = Depends(get_uow), 
                      current_user : domain.User = Depends(get_current_user)) -> List[schemas.Order] :
    with uow :
        orders = uow.orders.get_by_userid(userid = current_user.userid)

    return orders


@router.post('/{userid}/orders')
def request_order(userid : str,
                  order : schemas.OrderCreate, 
                  uow : Session = Depends(get_uow),
                  current_user : domain.User = Depends(get_current_user)) -> str :
    if userid != current_user.userid :
        raise HTTPException(status_code = 403, detial = 'Not authorized')
    orderid = order_crud.create_order(uow, 
                            userid = current_user.userid,
                            clothes_list = order.clothes_list,
                            )

    return orderid
    

@router.delete('/{userid}/orders/{orderid}')
def cancel_order(userid : str,
                 orderid : str,
                 uow : Session = Depends(get_uow),
                 current_user : domain.User = Depends(get_current_user)) :
    if userid != current_user.userid :
        raise HTTPException(status_code = 403, detial = 'Not authorized')
    
    order_crud.cancel_order(uow,
                            orderid
                            )

@router.get('/{userid}/orders/{orderid}')
def request_orderstatus(userid : str,
                        orderid : str,
                        uow : Session = Depends(get_uow),
                        current_user : domain.User = Depends(get_current_user)) -> schemas.OrderDisplay :
    if userid != current_user.userid :
        raise HTTPException(status_code = 403, detial = 'Not authorized')
    
    displayed_order = order_crud.get_order_status(uow, orderid)

    return displayed_order