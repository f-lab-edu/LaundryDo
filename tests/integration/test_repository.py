from src.dbmodel import (
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

class FakeSession :
    def __init__(self) :
        self.committed = False
    def commit(self) :
        self.committed = True


def test_register_new_user(dbmodel_user_factory, base_session) :
    user1 = dbmodel_user_factory()

    
    memory_repo = MemoryUserRepository()
    sa_repo = SqlAlchemyUserRepository(base_session)
    
    memory_repo.add(user1)
    sa_repo.add(user1)
    base_session.commit()

    assert memory_repo.get(user1.userid) == sa_repo.get(user1.userid)


def test_clothes_status_change(base_session, dbmodel_clothes_factory) :
    clothes = dbmodel_clothes_factory(clothesid = 'sample1')
    
    clothes_repo = SqlAlchemyClothesRepository(base_session)
    clothes_repo.add(clothes)
    base_session.commit()
    def launder(clothes) :
        clothes.status = ClothesState.DONE
        return clothes

    new_clothes = launder(clothes)
    clothes_repo.add(clothes) 
    base_session.commit() # session은 commit하면서 mapping된 class를 추적함.

    assert len(clothes_repo.list()) == 1


# TODO Memory Repo cannot recognize relationship
def test_memoryrepo_recognize_relationship(base_session, dbmodel_laundrybag_factory, dbmodel_clothes_factory) :
    num_clothes = 5

    laundrybag = dbmodel_laundrybag_factory(clothes_list = [dbmodel_clothes_factory() for _ in range(num_clothes)])

    sa_laundrybag_repo = SqlAlchemyLaundryBagRepository(base_session)
    sa_clothes_repo = SqlAlchemyClothesRepository(base_session)
    sa_laundrybag_repo.add(laundrybag)
    base_session.commit()

    assert len(sa_clothes_repo.list()) == num_clothes

    memory_laundrybag_repo = MemoryLaundryBagRepository()
    memory_clothes_repo = MemoryClothesRepository()
    memory_laundrybag_repo.add(laundrybag)

    assert len(memory_clothes_repo.list()) == num_clothes





    