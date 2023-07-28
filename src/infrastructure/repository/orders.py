from src.domain.repository import OrderRepository
from src.domain import Order, OrderState
from typing import List


class MemoryOrderRepository(OrderRepository) :        
    
    def __init__(self, orders : list = {}) :
        self._orders = {order.orderid : order for order in orders}

    def get(self, orderid : str) -> Order:
        return self._orders.get(orderid)

    def list(self) :
        return self._orders.values()

    def get_by_userid(self, userid : str) -> List[Order] :
        return [order for order in self._orders.values() if order._userid == userid]

    def get_by_status(self, status : OrderState) -> List[Order] : 
        return [order for order in self._orders.values() if order.status == status]
    
    def add(self, order: Order) :
        self._orders[order.orderid] = order



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