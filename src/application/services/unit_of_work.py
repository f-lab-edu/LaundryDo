import abc
from abc import abstractmethod

from src.domain.repository import  (
    UserRepository,
    OrderRepository,
    ClothesRepository,
    LaundryBagRepository,
    MachineRepository
)

from src.infrastructure.db.memory.repository import (
    MemoryClothesRepository,
    MemoryLaundryBagRepository,
    MemoryMachineRepository,
    MemoryOrderRepository,
    MemoryUserRepository
)



from src.infrastructure.db.sqlalchemy.setup import session
from src.infrastructure.db.sqlalchemy.repository import (
    SqlAlchemyClothesRepository,
    SqlAlchemyLaundryBagRepository,
    SqlAlchemyMachineRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyUserRepository
)

class AbstractUnitOfWork(abc.ABC):
    users : UserRepository
    orders : OrderRepository
    clothes : ClothesRepository
    laundrybags : LaundryBagRepository
    machines : MachineRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

class MemoryUnitOfWork(AbstractUnitOfWork) :
    users : MemoryUserRepository
    orders : MemoryOrderRepository
    clothes : MemoryClothesRepository
    laundrybags : MemoryLaundryBagRepository
    machines : MemoryMachineRepository

    def __init__(self, ) :
        self.users = MemoryUserRepository()
        self.orders = MemoryOrderRepository()
        self.clothes = MemoryClothesRepository()
        self.laundrybags = MemoryLaundryBagRepository()
        self.machines = MemoryMachineRepository()
        self.commited = False

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        self.committed = True

    @abc.abstractmethod
    def rollback(self):
        pass


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    users : UserRepository
    orders : OrderRepository
    clothes : ClothesRepository
    laundrybags : LaundryBagRepository
    machines : MachineRepository


    def __init__(self, session_factory = session):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory() 
        self.users = SqlAlchemyUserRepository(self.session)
        self.orders = SqlAlchemyOrderRepository(self.session)
        self.clothes = SqlAlchemyClothesRepository(self.session)
        self.laundrybags = SqlAlchemyLaundryBagRepository(self.session)
        self.machines = SqlAlchemyMachineRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()