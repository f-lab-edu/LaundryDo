from src.domain import (
    User,
    Order,
    Clothes,
    LaundryBag,
    Machine
)


from fastapi import FastAPI

app = FastAPI()




@app.get("/")
def root():
    return {"message": "welcome to LaundryDo"}


@app.post("/orders")
def request_order(new_order):
    return {"message": "request order"}


# @app.delete('/orders/{orderid}')
# def cancel_order(orderid : int) :
#     pass


@app.get("/orders")
def check_order_history():
    pass


@app.get("/orders/{orderid}")
def request_estimate_time(orderid: int):
    return orderid
