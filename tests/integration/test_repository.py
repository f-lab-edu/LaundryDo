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

from datetime import datetime
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
    machine.start(laundrybag, datetime.now())
    memory_machine_repo.add(machine)
    session.commit()

    assert memory_machine_repo.list() == [machine]
    assert memory_laundrybag_repo.get_by_status(status = LaundryBagState.RUNNING)
    assert memory_clothes_repo.get_by_status(status = ClothesState.PROCESSING)


def test_memoryrepo_recognize_orderstate_change_by_the_clothes(order_factory, laundrybag_factory, clothes_factory) :
    session = FakeSession()
    memory_order_repo = MemoryOrderRepository(session)
    memory_laundrybag_repo = MemoryLaundryBagRepository(session)
    memory_machine_repo = MemoryMachineRepository(session)

    clothes_states = [ClothesState.PREPARING, ClothesState.DISTRIBUTED, ClothesState.DISTRIBUTED, ClothesState.DISTRIBUTED]
    clothes_list = [clothes_factory(status = clothes_states[i], volume = 1) for i in range(len(clothes_states))]

    order = order_factory(clothes_list = clothes_list)
    memory_order_repo.add(order)
    session.commit()

    # put in laundry bag
    laundrybag = laundrybag_factory(clothes_list = clothes_list)
    memory_laundrybag_repo.add(laundrybag)
    assert memory_order_repo.get_by_status(status = OrderState.PREPARING) == [order]

    # put the laundrybag in machine
    machine = Machine(machineid = 'sample-machine')
    machine.start(laundrybag, datetime.now())
    memory_machine_repo.add(machine)
    session.commit()

    assert memory_order_repo.get_by_status(status = OrderState.WASHING) == [order]


def test_sa_repo_get_orderstate_determined_by_earliest_clothesstate(order_factory, clothes_factory, session) :
    '''
    put clothes with different states in different orders.
    test if the status of order is determined by the earliest clothes state.
    e.g) order w/ clothes_list = [before washing, after washing] => order state will be before washing.
    '''
    
    sa_order_repo = SqlAlchemyOrderRepository(session)
    sa_clothes_repo = SqlAlchemyClothesRepository(session)
    clothesstate = [ClothesState.DONE, ClothesState.DONE, ClothesState.DONE, ClothesState.PREPARING, ClothesState.PREPARING]
    
    clothes = [clothes_factory(status = clothesstate[i]) for i in range(len(clothesstate))]
    
    orders = [order_factory() for i in range(len(clothesstate))]

    for i, order in enumerate(orders) :
        order.clothes_list.append(clothes[i])
    
    orderstates = [OrderState.RECLAIMING, OrderState.RECLAIMING, OrderState.RECLAIMING, OrderState.PREPARING, OrderState.PREPARING]
    print(orders)
    for i, order in enumerate(orders) :
        sa_order_repo.add(order)
        # assert order.clothes_list == [clothes[i]
        assert orderstates[i] == order.status
    session.commit()

    print(sa_order_repo.list())

    assert len(sa_order_repo.list()) == 5
    assert len(sa_order_repo.get_by_status(status = OrderState.RECLAIMING)) == 3