from src.domain.repository import (
    UserRepository,
    OrderRepository,
    ClothesRepository,
    LaundryBagRepository,
    MachineRepository
)

from src.domain import (
    User,
    Order,
    Clothes,
    LaundryBag,
    Machine,
    OrderState,
    MachineState,
    ClothesState,
    LaundryBagState
)


class SqlAlchemyUserRepository(UserRepository) :

    def __init__(self, session) :
        self.session = session

    def get(self, userid : str) -> User:
        return self.session.query(User).filter_by(userid = userid).one()

    def list(self) :
        return self.session.query(User).all()
    
    def add(self, user: User) :
        self.session.add(user)


class SqlAlchemyOrderRepository(OrderRepository) :        
    
    def __init__(self, session) :
        self.session = session

    def get(self, orderid : str) -> Order:
        return self.session.query(Order).filter_by(orderid = orderid).one()

    def list(self) :
        return self.session.query(Order).all()
    
    def add(self, order : Order) :
        self.session.add(order)


class SqlAlchemyClothesRepository(ClothesRepository) :
    
    def __init__(self, session) :
        self.session = session

    def get(self, clothesid : str) -> Clothes :
        return self.session.query(Clothes).filter_by(clothesid = clothesid).one()

    def get_by_status(self, status : ClothesState) -> Clothes :
        return self.session.query(Clothes).filter_by(status = status).all()

    def list(self) :
        return self.session.query(Clothes).all()
    
    def add(self, clothes : Clothes) :
        self.session.add(clothes)


class SqlAlchemyLaundryBagRepository(LaundryBagRepository) : 
    
    def __init__(self, session) :
        self.session = session

    def get(self, laundrybagid : str) -> User:
        return self.session.query(LaundryBag).filter_by(laundrybagid = laundrybagid).one()

    def get_by_status(self, status : LaundryBagState) -> LaundryBag :
        return self.session.query(LaundryBag).filter_by(status = status).all()

    def list(self) :
        return self.session.query(LaundryBag).all()
    
    def add(self, laundrybag : LaundryBag) :
        self.session.add(laundrybag)


class SqlAlchemyMachineRepository(MachineRepository) :
    
    def __init__(self, session) :
        self.session = session

    def get(self, machineid : str) -> User:
        return self.session.query(Machine).filter_by(machineid = machineid).one()

    def get_by_status(self, status : MachineState) -> Machine :
        return self.session.query(Machine).filter_by(status = status).all()


    def list(self) :
        return self.session.query(Machine).all()
    
    def add(self, machine: Machine) :
        self.session.add(machine)
