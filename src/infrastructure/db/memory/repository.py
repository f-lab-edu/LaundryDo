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


class MemoryUserRepository(UserRepository) :

    def __init__(self) :
        self.session = {}

    def get(self, userid : str) -> User:
        return self.session.get(userid)

    def list(self) :
        return self.session.values()
    
    def add(self, user: User) :
        self.session[user.id] = user





class MemoryOrderRepository(OrderRepository) :        
    
    def __init__(self) :
        self.session = {}

    def get(self, orderid : str) -> Order:
        return self.session.get(orderid)

    def list(self) :
        return self.session.values()
    
    def add(self, order: Order) :
        self.session[order.id] = order





class MemoryClothesRepository(ClothesRepository) :
    
    def __init__(self) :
        self.session = {}

    def get(self, clothesid : str) -> Clothes :
        return self.session.get(clothesid)

    def get_by_status(self, status : ClothesState) -> Clothes :
        return [clothes for clothes in self.session.values() if clothes.status == status]

    def list(self) :
        return self.session.values()
    
    def add(self, clothes : Clothes) :
        self.session[clothes.id] = clothes





class MemoryLaundryBagRepository(LaundryBagRepository) : 
    
    def __init__(self) :
        self.session = {}

    def get(self, laundrybagid : str) -> LaundryBagState :
        return self.session.get(laundrybagid)

    def get_by_status(self, status : LaundryBagState) -> LaundryBag :
        return [laundrybag for laundrybag in self.session.values() if laundrybag.status == status]

    def list(self) :
        return self.session.values()
    
    def add(self, laundrybag : LaundryBag) :
        self.session[laundrybag.id] = laundrybag




class MemoryMachineRepository(MachineRepository) :
    
    def __init__(self) :
        self.session = {}

    def get(self, machineid : str) -> Machine :
        return self.session.get(machineid)

    def get_by_status(self, status : MachineState) -> Machine :
        return [machine for machine in self.session.values() if machine.status == status]

    def list(self) :
        return self.session.values()
    
    def add(self, machine : Machine) :
        self.session[machine.id] = machine
