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
    SqlAlchemyMachineRepository
)

import pytest

class FakeSession :
    def __init__(self) :
        self.committed = False
    def commit(self) :
        self.committed = True


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
@pytest.mark.skip
def test_memoryrepo_recognize_relationship(session, laundrybag_factory, clothes_factory) :
    num_clothes = 5

    laundrybag = laundrybag_factory(clothes_list = [clothes_factory() for _ in range(num_clothes)])

    sa_laundrybag_repo = SqlAlchemyLaundryBagRepository(session)
    sa_clothes_repo = SqlAlchemyClothesRepository(session)
    sa_laundrybag_repo.add(laundrybag)
    session.commit()

    assert len(sa_clothes_repo.list()) == num_clothes

    memory_laundrybag_repo = MemoryLaundryBagRepository()
    memory_clothes_repo = MemoryClothesRepository()
    memory_laundrybag_repo.add(laundrybag)

    assert len(memory_clothes_repo.list()) == num_clothes

    



    