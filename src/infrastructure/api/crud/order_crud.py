from src.application.unit_of_work import AbstractUnitOfWork
from src.domain.order import OrderState


def update_orderstate(uow : AbstractUnitOfWork, orderstate : OrderState) :
    with uow :
        orders = uow.orders.get_by_status(status = orderstate)
        for order in orders :
            order.update_status()
            uow.commit()
        uow.commit()