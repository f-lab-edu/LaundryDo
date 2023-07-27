from abc import ABC, abstractmethod

from src.domain import User, Order, Clothes, LaundryBag, Machine
from typing import List

class UserRepository(ABC) :
    @abstractmethod
    def get(self, userid) -> User:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, user: User) :
        raise NotImplementedError


class OrderRepository(ABC) :        
    @abstractmethod
    def get(self, orderid) -> Order:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, order: Order) :
        raise NotImplementedError


class ClothesRepository(ABC) :
    @abstractmethod
    def get(self, clothesid) -> Clothes:
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, clothes: Clothes) :
        raise NotImplementedError


class LaundryBagRepository(ABC) : 
    @abstractmethod
    def get(self, laundrybagid) -> LaundryBag :
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, laundryBag: LaundryBag) :
        raise NotImplementedError


class MachineRepository(ABC) :
    @abstractmethod
    def get(self, machineid) -> Machine :
        raise NotImplementedError
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, machine : Machine) :
        raise NotImplementedError
