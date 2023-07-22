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
    LaundryBagState,
    LaundryLabel,
    laundrybag
)

from typing import List

class MemoryUserRepository(UserRepository) :

    def __init__(self, users : dict = {}) :
        self._users = users

    def get(self, userid : str) -> User:
        return self._users.get(userid)

    def list(self) :
        return self._users.values()
    
    def add(self, user: User) :
        self._users[user.userid] = user





class MemoryOrderRepository(OrderRepository) :        
    
    def __init__(self, orders : list) :
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





class MemoryClothesRepository(ClothesRepository) :
    
    def __init__(self, clothes_dict : dict = {}) :
        self._clothes_dict = clothes_dict

    def get(self, clothesid : str) -> Clothes :
        return self._clothes_dict.get(clothesid)

    def get_by_status(self, status : ClothesState) -> List[Clothes]  :
        return [clothes for clothes in self._clothes_dict.values() if clothes.status == status]

    def list(self) :
        return self._clothes_dict.values()
    
    def add(self, clothes : Clothes) :
        self._clothes_dict[clothes.clothesid] = clothes





class MemoryLaundryBagRepository(LaundryBagRepository) : 
    
    def __init__(self, laundrybags : List = []) :
        self._laundrybags = {laundrybag.laundrybagid : laundrybag for laundrybag in laundrybags}

    def get(self, laundrybagid : str) -> LaundryBag :
        return self._laundrybags.get(laundrybagid)

    def get_by_status(self, status : LaundryBagState) -> List[LaundryBag] :
        return [laundrybag for laundrybag in self._laundrybags.values() if laundrybag.status == status]

    def get_waitingbag_by_label(self, label : LaundryLabel) -> LaundryBag :
        '''
        get list of laundrybags that are LaundryBagState.READY and LaundryLabel
        '''
        return next((laundrybag for laundrybag in self._laundrybags.values() 
                    if laundrybag.status == LaundryBagState.COLLECTING and laundrybag.label == label), None)

    def list(self) :
        return self._laundrybags.values()
    
    def add(self, laundrybag : LaundryBag) :
        self._laundrybags[laundrybag.laundrybagid] = laundrybag




class MemoryMachineRepository(MachineRepository) :
    
    def __init__(self, machines : dict = {} ) :
        self._machines = {}

    def get(self, machineid : str) -> Machine :
        return self._machines.get(machineid)

    def get_by_status(self, status : MachineState) -> List[Machine] :
        return [machine for machine in self._machines.values() if machine.status == status]

    def list(self) :
        return self._machines.values()
    
    def add(self, machine : Machine) :
        self._machines[machine.machineid] = machine
