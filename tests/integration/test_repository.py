from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    ClothesState,
    LaundryBag,
    Machine
)

from src.infrastructure.repository import (
    MemoryUserRepository,
    MemoryOrderRepository,
    MemoryClothesRepository,
    MemoryLaundryBagRepository,
    MemoryMachineRepository
)

from src.infrastructure.repository import (
    SqlAlchemyUserRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyClothesRepository,
    SqlAlchemyLaundryBagRepository,
    SqlAlchemyMachineRepository,
    FakeSession
)

import pytest



def test_register_new_user(user_factory, session) :
    user1 = user_factory()

    
    memory_repo = MemoryUserRepository()
    sa_repo = SqlAlchemyUserRepository(session)
    
    memory_repo.add(user1)
    sa_repo.add(user1)
    session.commit()

    assert memory_repo.get(user1.userid) == sa_repo.get(user1.userid)


def test_clothes_status_change(session, clothes_factory) :
    clothes = clothes_factory(clothesid = 'sample1')
    
    clothes_repo = SqlAlchemyClothesRepository(session)
    clothes_repo.add(clothes)
    session.commit()
    def launder(clothes) :
        clothes.status = ClothesState.DONE
        return clothes

    new_clothes = launder(clothes)
    clothes_repo.add(clothes) 
    session.commit() # session은 commit하면서 mapping된 class를 추적함.

    assert len(clothes_repo.list()) == 1


# TODO Memory Repo cannot recognize relationship
def test_memoryrepo_recognize_order_clothes_relationship(order_factory, clothes_factory) :
    num_clothes = 5

    session = FakeSession()

    memory_clothes_repo = MemoryClothesRepository(session)
    memory_order_repo = MemoryOrderRepository(session)

    order = order_factory(clothes_list = [clothes_factory() for _ in range(num_clothes)])


    memory_order_repo.add(order)

    
    session.commit()

    assert len(memory_order_repo.list()) == 1
    assert len(memory_clothes_repo.list()) == num_clothes

    # order changes clothes state.
    assert len(memory_clothes_repo.get_by_status(status = ClothesState.PREPARING)) == num_clothes


    