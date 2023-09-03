from sqlalchemy import select

from src.domain.repository import AbstractOrderRepository
from src.domain import Order, OrderState, Clothes
from .session import FakeSession
from typing import List


class MemoryOrderRepository(AbstractOrderRepository) :        
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, orderid : str) -> Order:
        return self.session.query(Order).get(orderid)

    def list(self) :
        return list(self.session.query(Order).values())

    def get_by_userid(self, userid : str) -> List[Order] :
        return self.session.query(Order).filter_by(userid = userid)

    def get_by_status(self, status : OrderState) -> List[Order] : 
        return self.session.query(Order).filter_by(status = status)
    
    def add(self, order: Order) :
        self.session.buffers[Order][order.orderid] = order



class SqlAlchemyOrderRepository(AbstractOrderRepository) :        
    
    def __init__(self, session) :
        self.session = session

    def get(self, orderid : str) -> Order:
        return self.session.query(Order).filter_by(orderid = orderid).one()

    def get_by_userid(self, userid : str) -> List[Order] :
        return self.session.query(Order).filter_by(userid = userid).all()

    def get_by_orderid(self, orderid : str) -> Order :
        return self.session.query(Order).filter_by(orderid = orderid).one()

    def get_by_status(self, status : OrderState) -> List[Order] :
        # return self.session.query(Order).filter(Order.status == status).all()
        return self.session.query(Order).filter_by(status = status).all()
    
        # return self.session.query(Clothes, Order).filter(Order.orderid == Clothes.orderid).filter(Order.status == status).all()
        # return self.session.execute()#.all()
        

    def list(self) :
        return self.session.query(Order).all()
    
    def add(self, order : Order) :
        self.session.add(order)