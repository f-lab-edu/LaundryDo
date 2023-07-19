from src.domain import Order

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome to LaundryDo"}


@app.post("/orders/")
def request_order(new_order):
    return new_order


# @app.delete('/orders/{orderid}')
# def cancel_order(orderid : int) :
#     pass


# @app.get("/orders")
# def check_order_history(order):
#     return order


@app.get("/orders/{orderid}")
def request_estimate_time(orderid: int):
    return orderid
