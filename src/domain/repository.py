from abc import ABC, abstractmethod

from src.domain import User, Order, Clothes, LaundryBag, Machine
from typing import List

class AbstractUserRepository(ABC) :
    @abstractmethod
    def get(self, userid) -> User:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, user: User) :
        raise NotImplementedError


class AbstractOrderRepository(ABC) :        
    @abstractmethod
    def get(self, orderid) -> Order:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, order: Order) :
        raise NotImplementedError


class AbstractClothesRepository(ABC) :
    @abstractmethod
    def get(self, clothesid) -> Clothes:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, clothes: Clothes) :
        raise NotImplementedError


class AbstractLaundryBagRepository(ABC) : 
    @abstractmethod
    def get(self, laundrybagid) -> LaundryBag :
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, laundryBag: LaundryBag) :
        raise NotImplementedError


class AbstractMachineRepository(ABC) :
    @abstractmethod
    def get(self, machineid) -> Machine :
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, machine : Machine) :
        raise NotImplementedError
