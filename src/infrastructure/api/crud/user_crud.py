from sqlalchemy.orm import Session

from src.domain.user import User
from src.infrastructure.api import schemas

def create_user(db : Session, user_create : schemas.UserCreate) :
    db_user = User(userid = user_create.userid, 
         password = user_create.password1,
         phone_number = user_create.phone_number,
         address = user_create.address
         )
    
    db.add(db_user)
    db.commit()