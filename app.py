from src.domain import Order
from enum import Enum

from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel
app = FastAPI()

class Order(BaseModel) :
    userid : str
    clothes_list : list | None = None




orders = {'eunsung' : {
        'order_list' : [
            {'orderid' : 1,
            'clothes' : [{'clothesid' : 1, 'label' : 'wash'},],
            },
            ]
        },
    }

class Ordertype(str, Enum) :
    REQUEST = 'request'
    CANCEL = 'cancel'

@app.get("/")
def root():
    return {"message": "welcome to LaundryDo"}



# @app.delete('/orders/{orderid}')
# def cancel_order(orderid : int) :
#     pass


# @app.get("/orders")
# def check_order_history(order):
#     return order


# @app.get("/orders/{orderid}/")
# def request_estimate_time(orderid: int):
#     return orders[orderid]

@app.get('/ordertype/{ordertype}') 
def request_type(ordertype : Ordertype) :
    if ordertype is Ordertype.REQUEST :
        return ordertype
    else :
        print(ordertype)

@app.get("/files/{file_path:path}")
def read_file(file_path : str) :
    with open(file_path, 'r') as f :
        file = f.readlines()
    
    return file




@app.get("/orders/{userid}")
def request_clothes(userid : str, orderid : int, clothesid : int) :
    return orders[userid]['order_list'][orderid]['clothes'][clothesid]

@app.post('/new-orders/')
def request_order(order : Order) :
    orders[order.userid] = {'new_order'}
    return orders

@app.get('/users/')
def request_userid(userid : Annotated[str | None, Query(max_length = 50 )]) :
    return orders[userid]

