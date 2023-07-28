from src.domain.repository import OrderRepository
from src.domain import Order, OrderState
from .session import FakeSession
from typing import List


class MemoryOrderRepository(OrderRepository) :        
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, orderid : str) -> Order:
        return self.session.query(Order).get(orderid)

    def list(self) :
        return self.session.query(Order).values()

    def get_by_userid(self, userid : str) -> List[Order] :
        return self.session.query(Order).filter_by(userid = userid)

    def get_by_status(self, status : OrderState) -> List[Order] : 
        return self.session.query(Order).filter_by(status = status)
    
    def add(self, order: Order) :
        self.session.buffers[Order][order.orderid] = order



class SqlAlchemyOrderRepository(OrderRepository) :        
    
    def __init__(self, session) :
        self.session = session

    def get(self, orderid : str) -> Order:
        return self.session.query(Order).filter_by(orderid = orderid).one()

    def get_by_userid(self, userid : str) -> List[Order] :
        return self.session.query(Order).filter_by(userid = userid).all()

    def get_by_orderid(self, orderid : str) -> Order :
        return self.session.query(Order).filter_by(orderid = orderid).one()

    def get_by_status(self, status : OrderState) -> List[Order] :
        return self.session.query(Order).filter_by(status = status).all()

    def list(self) :
        return self.session.query(Order).all()
    
    def add(self, order : Order) :
        self.session.add(order)