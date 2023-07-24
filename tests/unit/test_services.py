from src.domain.services import (
    request_order,
    cancel_order,
    distribute_order,
    put_in_laundrybag,
    reclaim_clothes_into_order,
    get_clothes_in_process,
    allocate,
    ship
)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True



def test_request_order(order_factory) :
    pass

def test_allocate_laundrybag() :
    pass

def recliaim_clothes_into_order() :
    pass