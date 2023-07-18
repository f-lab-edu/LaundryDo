from .clothes import ClothesState
from .order import Order, OrderState

from typing import List

class User :
    def __init__(self, userid: str, address: str, orderlist : List[Order] = []) :
        self.userid = userid
        self.address = address
        self.orderlist = orderlist


    def __repr__(self) :
        return f"{self.__class__.__name__} id= {self.userid}, address= {self.address}"

    
    def __hash__(self) :
        return hash(self.userid)

    def __eq__(self, other) :
        if self.__class__ == other.__class__ :
            return self.userid == other.userid


    def request_order(self, order: Order):
        order.status = OrderState.PREPARING
        self.orderlist.append(order)

    def cancel_order(self, order: Order):
        [selected_order] = [
            submitted_order
            for submitted_order in self.orderlist
            if order == submitted_order
        ]


        if selected_order and (selected_order.status == OrderState.PREPARING or selected_order.status == OrderState.SENDING) :
            selected_order.status = OrderState.CANCELLED
            # update clothes status
            for clothes in selected_order :
                clothes.status = ClothesState.CANCELLED

        else :
            print(f'order id {order.id} does not exist. OR order in the laundry cannot be cancelled. your order is in [{selected_order.status}]')

    def request_order_status(self, query_order : Order) :
        for order in self.orderlist :
            if order == query_order :
                return order.status
        raise ValueError(f'{query_order} cannot be found.')
                
    def request_order_history(self) :
        return self.orderlist
