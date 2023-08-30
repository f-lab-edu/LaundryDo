from fastapi import APIRouter, Depends
from starlette import status
from src.infrastructure.fastapi import schemas
from src.infrastructure.db.sqlalchemy.setup import get_db

router = APIRouter(
    prefix = '/user/'
)

@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create : ) :



@app.get('/users/{userid}/orders', response_model = schemas.Order)
async def request_orderlist(userid : str, session : Session = Depends(get_db)) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        return uow.orders.get_by_userid(userid=userid)