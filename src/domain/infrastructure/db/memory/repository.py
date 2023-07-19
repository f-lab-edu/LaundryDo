from domain.repository import (
    UserRepository,
    OrderRepository,
    ClothesRepository,
    LaundryBagRepository,
    MachineRepository
)

class MemoryUserRepository(UserRepository) :
    pass


class MemoryOrderRepository(OrderRepository) :
    pass


class MemoryClothesRepository(ClothesRepository) : 
    pass


class MemoryLaundryBagRepository(LaundryBagRepository) :
    pass

    
class MemoryMachineRepository(MachineRepository) :
    pass