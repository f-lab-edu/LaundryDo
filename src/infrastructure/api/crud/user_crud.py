from sqlalchemy.orm import Session
from src.application.unit_of_work import SqlAlchemyUnitOfWork

from src import domain
from src.infrastructure.api import schemas
from src.infrastructure.api.auth import pwd_context



def create_user(uow : SqlAlchemyUnitOfWork, user_create : schemas.UserCreate) :
    
    with uow :
        db_user = domain.User(userid = user_create.userid, 
            password = pwd_context.hash(user_create.password1),
            phone_number = user_create.phone_number,
            address = user_create.address
            )
        uow.users.add(db_user)
        uow.commit()

def get_existing_user(uow: SqlAlchemyUnitOfWork, user_create : schemas.UserCreate) : 
    with uow :
        existed_user = uow.users.get(userid = user_create.userid)
    return existed_user
    

def get_user(uow: SqlAlchemyUnitOfWork, userid : str) -> domain.User :
    with uow :
        existed_user = uow.users.get(userid = userid)
    return existed_user
    

