import abc
from abc import abstractmethod

from src.domain.repository import  (
    UserRepository,
    OrderRepository,
    ClothesRepository,
    LaundryBagRepository,
    MachineRepository,
)

from src.infrastructure.repository import (
    MemoryClothesRepository,
    MemoryLaundryBagRepository,
    MemoryMachineRepository,
    MemoryOrderRepository,
    MemoryUserRepository,
    FakeSession
)



from src.infrastructure.db.sqlalchemy.setup import session
from src.infrastructure.repository import (
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

    def __enter__(self):
        return self

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

    def __init__(self, session : FakeSession) :
        self.session = session
        self.users = MemoryUserRepository(self.session)
        self.orders = MemoryOrderRepository(self.session)
        self.clothes = MemoryClothesRepository(self.session)
        self.laundrybags = MemoryLaundryBagRepository(self.session)
        self.machines = MemoryMachineRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


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