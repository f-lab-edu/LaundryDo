from abc import ABC, abstractmethod

from model import Clothes
from typing import List

class UserRepository(ABC) :
    def __init__(self) :
    
    @abstractmethod
    def get(self, user) :
        raise NotImplementedError
    @abstractmethod
    def all(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, user) :
        raise NotImplementedError


class OrderRepository(ABC) :
    def __init__(self) :
        
    @abstractmethod
    def get(self, order) :
        raise NotImplementedError
    @abstractmethod
    def all(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, order) :
        raise NotImplementedError

class ClothesRepository(ABC) :
    def __init__(self) :
        
    @abstractmethod
    def get(self, order) :
        raise NotImplementedError
    @abstractmethod
    def all(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, order) :
        raise NotImplementedError

class LaundryBagRepository(ABC) : 
    def __init__(self) :
        
    @abstractmethod
    def get(self, order) :
        raise NotImplementedError
    @abstractmethod
    def all(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, order) :
        raise NotImplementedError

class MachineRepository(ABC) :
    def __init__(self) :
    
    @abstractmethod
    def get(self, machine) :
        raise NotImplementedError
    @abstractmethod
    def all(self) :
        raise NotImplementedError
    @abstractmethod
    def add(self, machine) :
        raise NotImplementedError
