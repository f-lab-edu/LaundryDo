from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from datetime import datetime
from datetime import timedelta
from typing import List
from src.infrastructure.api import schemas
from src.infrastructure.api.crud.user_crud import pwd_context
from src.infrastructure.db.setup import get_uow
from src import domain



from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.application import services
from src.infrastructure.api.crud import user_crud, order_crud

from sqlalchemy.orm import Session

from config import APIConfigurations


from logging import getLogger

logger = getLogger(__name__)





router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "65cea85d36060df1841ba5689840b0da447100ed823ab7e3b610c447c9a497d0" # create using openssl rand -hex 32
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = f'/v{APIConfigurations.version}/user/login')



@router.post("/login")
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
    



@router.get('/list')
def list_user(uow : SqlAlchemyUnitOfWork = Depends(get_uow)) -> List[schemas.User] :
    with uow :
        all_users = uow.users.list()
        all_users = [schemas.User.model_validate(user) for user in all_users]
    return all_users
    
    
    


@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
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


@router.post('/{userid}/orders', status_code = status.HTTP_204_NO_CONTENT)
def request_order(order : schemas.OrderCreate, 
                  uow : Session = Depends(get_uow),
                  current_user : domain.User = Depends(get_current_user)) :
 
    order_crud.create_order(uow, 
                            userid = current_user.userid,
                            clothes_list = order.clothes_list,
                            )
    