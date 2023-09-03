from fastapi import APIRouter, Body, Depends
from starlette import status

from datetime import datetime
from typing import List, Dict, Annotated

from src.application.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.db.setup import get_db
from src.infrastructure.api import schemas
from src.application import services
from sqlalchemy.orm import Session


router = APIRouter()



@router.get('/{userid}/{orderid}')
async def request_order_info(userid : str, orderid : str, session : Session = Depends(get_db)) -> schemas.Order : ## TODO : orders only be accessible for one user.
    '''
    request estimate time for order in process. if order is done or cancelled, return 0.
    '''
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        return uow.orders.get_by_orderid(orderid = orderid)


@router.post('/users/{userid}/orders', response_model = schemas.Order)
async def request_order(userid : str, order : Annotated[ schemas.Order, 
            Body(
                examples = [
                    {   
                        'userid' : '[userid]',
                        "orderid" : '[userid]-order-[num]',
                        "description" : "세탁 요청한 옷들의 리스트가 담긴 주문 정보",
                        'clothes_list' : [{
                            "clothesid" : "흰티셔츠",
                            "label" : "드라이클리닝",
                            "volume" : 3,
                                }
                            ],
                        "received_at" : datetime(2023, 7, 21, 10, 11),
                    }
                ]
            )
        ], 
        session : Session = Depends(get_db)
    ) :
    uow = SqlAlchemyUnitOfWork(session)
    with uow :
        services.request_order(uow,**dict(order))
        uow.commit()

    return order


@router.put('/{orderid}', status_code = status.HTTP_204_NO_CONTENT)
async def cancel_order(userid : str, orderid : str, session : Session = Depends(get_db)) :#-> schemas.Order :
    uow = SqlAlchemyUnitOfWork(session)
    
    with uow :
        order = services.cancel_order(uow, userid, orderid)
        order = schemas.Order.model_validate(order)
        order.commit()

