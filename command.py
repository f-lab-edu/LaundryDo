from model import Order

class Command :
    pass

class RequestOrderCommand(Command) :
    order : Order