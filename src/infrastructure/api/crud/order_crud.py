from src.application.unit_of_work import AbstractUnitOfWork
from src.domain.order import OrderState
from src import domain
from src.infrastructure.api import schemas
from typing import List
from datetime import datetime
from uuid import uuid4


def update_orderstate(uow : AbstractUnitOfWork, orderstate : OrderState) :
    with uow :
        orders = uow.orders.get_by_status(status = orderstate)
        for order in orders :
            order.update_status()
            uow.commit()
        uow.commit()

def create_order(uow : AbstractUnitOfWork, userid : str, clothes_list : List[schemas.Clothes]) :
    with uow :
        new_order = domain.Order(orderid = f'orderid-{userid}-{str(uuid4())[:4]}',
                             userid = userid,
                             clothes_list = [domain.Clothes(clothesid = clothes.clothesid,
                                                            label = clothes.label,
                                                            volume = clothes.volume)  \
                                                            for clothes in clothes_list],
                             received_at = datetime.now())
        uow.orders.add(new_order)
        uow.commit()