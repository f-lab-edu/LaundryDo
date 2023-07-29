from src.domain import (
    User,
    Order,
    OrderState,
    Clothes,
    ClothesState,
    LaundryBag,
    LaundryLabel,
    LaundryBagState,
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

    fakesession = FakeSession()
    memory_repo = MemoryUserRepository(fakesession)
    sa_repo = SqlAlchemyUserRepository(session)
    
    memory_repo.add(user1)
    sa_repo.add(user1)
    
    fakesession.commit()
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
def test_memoryrepo_recognize_clothes_order_relationship(order_factory, clothes_factory) :
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


def test_memoryrepo_recognize_clothes_laundrybag_relationship(clothes_factory, laundrybag_factory) :
    num_clothes = 5

    session = FakeSession()

    memory_clothes_repo = MemoryClothesRepository(session)
    memory_laundrybag_repo = MemoryLaundryBagRepository(session)
    
    laundrybag = laundrybag_factory(clothes_list = [])
    
    clothes_bulk = []
    for _ in range(num_clothes) :
        clothes = clothes_factory(volume = 1, label = LaundryLabel.DRY) # all clothes can be contained in one bag
        clothes_bulk.append(clothes)
        memory_clothes_repo.add(clothes)
    session.commit()

    # put in laundrybag
    for clothes in clothes_bulk :
        laundrybag.append(clothes)

    memory_laundrybag_repo.add(laundrybag)
    session.commit()

    assert len(memory_clothes_repo.get_by_status(status = ClothesState.DISTRIBUTED)) == 5
        
def test_memory_repo_recognize_clothes_machine_relationship(clothes_factory, laundrybag_factory) :
    session = FakeSession()

    memory_clothes_repo = MemoryClothesRepository(session)
    memory_laundrybag_repo = MemoryLaundryBagRepository(session)
    memory_machine_repo = MemoryMachineRepository(session)

    ## somehow laundrybag is full and its state changed to READY.
    laundrybag = laundrybag_factory(clothes_list = [clothes_factory(volume = 1, label = LaundryLabel.DRY) \
                                                        for _ in range(3)], 
                                    status = LaundryBagState.READY
                                    )
    
    memory_laundrybag_repo.add(laundrybag)
    session.commit()
    assert memory_laundrybag_repo.get_by_status(status = LaundryBagState.READY)

    machine = Machine(machineid = 'sample-machine')
    machine.put(laundrybag)
    memory_machine_repo.add(machine)
    session.commit()

    assert memory_machine_repo.list() == [machine]
    assert memory_laundrybag_repo.get_by_status(status = LaundryBagState.RUN)
    assert memory_clothes_repo.get_by_status(status = ClothesState.PROCESSING)


def test_memoryrepo_recognize_orderstate_changes_by_the_process(order_factory, ) :
    '''what standard does order should follow? clothes?'''
    pass