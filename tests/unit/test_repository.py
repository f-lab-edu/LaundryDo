from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    ClothesState,
    LaundryBag,
    Machine
)

from src.infrastructure.db.memory.repository import (
    MemoryUserRepository,
    MemoryOrderRepository,
    MemoryClothesRepository,
    MemoryLaundryBagRepository,
    MemoryMachineRepository
)

from src.infrastructure.db.sqlalchemy.repository import (
    SqlAlchemyUserRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyClothesRepository,
    SqlAlchemyLaundryBagRepository,
    SqlAlchemyMachineRepository
)


def test_register_new_user(user_factory, session) :
    user1 = user_factory()

    
    memory_repo = MemoryUserRepository()
    sa_repo = SqlAlchemyUserRepository(session)
    
    memory_repo.add(user1)
    sa_repo.add(user1)

    assert memory_repo.get(user1.userid) == sa_repo.get(user1.userid)

