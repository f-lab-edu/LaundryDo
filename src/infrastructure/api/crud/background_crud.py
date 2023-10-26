from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRY_MINVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from src.domain.clothes import Clothes, ClothesState, LaundryLabel
from src.domain.order import Order, OrderState, clothes_order_mapping
from src.domain.laundrybag import LaundryBag, LaundryBagState
from src.domain.machine import Machine, MachineState
from src.domain.repository import AbstractOrderRepository, AbstractLaundryBagRepository, AbstractMachineRepository
from src.application.unit_of_work import AbstractUnitOfWork

from src.infrastructure.api.crud import order_crud

from collections import deque
from typing import List, Dict
from datetime import datetime
from uuid import uuid4

from collections import deque, defaultdict

###################
# Scheduling Jobs #
###################


def update_laundrybag_state(uow : AbstractUnitOfWork) :
    print('update_laundrybag_state')
    with uow :
        laundrybags_collecting = uow.laundrybags.get_by_status(status = LaundryBagState.COLLECTING)
        
        for laundrybag in laundrybags_collecting : 
            if laundrybag.created_at - datetime.now() >= LAUNDRYBAG_MAX_WAITINGTIME :
                laundrybag.status = LaundryBagState.READY
                uow.commit()





def allocate_laundrybag_to_machine(uow : AbstractUnitOfWork) :
    '''put laundrybag into available machine 
        ready_laundrybag_list = get_laundrybags()
        while get_available_machine() := machine :
            machine.start( ready_laundrybag_list.pop(), exec_time )
    '''
    print('allocate laundrybag_to_machine')
    with uow :
        laundrybags_in_ready = deque(sorted(uow.laundrybags.get_by_status(status=LaundryBagState.READY)))
        
        available_machines = deque(sorted(uow.machines.get_by_status(status = MachineState.READY)))
        
        print(f'available machines : {available_machines}')
        print(f'laundrybags in ready : {laundrybags_in_ready}')

        while available_machines and laundrybags_in_ready :
            print('matching laundrybag to machine...')
            machine = available_machines.popleft()
            laundrybag = laundrybags_in_ready.popleft()
            machine.start(laundrybag)
        uow.commit()
    # update order state
    order_crud.update_orderstate(uow, orderstate = OrderState.PREPARING)




def update_machine_state_if_laundry_done(uow : AbstractUnitOfWork) :
    '''
    update Machine(RUNNING), if the remainingTime == 0
    '''
    print('update_machine_state_if_laundry_done')
    with uow : 
        machines_in_progress = uow.machines.get_by_status(status = MachineState.RUNNING)
        for machine in machines_in_progress :
            machine.update_runtime()
            machine.update_status()

            uow.commit()

    order_crud.update_orderstate(uow, orderstate = OrderState.WASHING)



def reclaim_clothes_from_machine(uow : AbstractUnitOfWork) :
    '''RECLAIM CLOTHES FROM MACHINE IF DONE
    update_machine_status(exec_time)
    machines = get_machine_done()
    for machine in machines :
        # update laundrybag status -> laundrybag DB에 이름 어떻게 할지. 재활용 혹은 재생성
        machine.contained.status = DONE
        for clothes in machine.contained.clothes_list :
            clothes.status = DONE
    '''
    print('reclaim_clothes_from_machine')
    with uow :
        finished_machines = uow.machines.get_by_status(status = MachineState.DONE)
        for machine in finished_machines :
            for clothes in machine.contained.clothes_list :
                clothes.status = ClothesState.RECLAIMED
                print(f'{clothes} is out of {machine}.')
                uow.clothes.add(clothes)
            # update laundrybag state
            laundrybag = machine.contained
            laundrybag.status = LaundryBagState.COLLECTING
            machine.contained = None
            machine.status = MachineState.READY
        uow.commit()
    order_crud.update_orderstate(uow, orderstate = OrderState.RECLAIMING)



def ship_finished_order(uow : AbstractUnitOfWork) : 
    '''SHIP
    reclaimed_orders = get_order_reclaimed()
    for order in reclaimed_orders :
        order.ship() # change order status to SHIP_READY
    '''
    print('ship_finished_order')
    order_crud.update_orderstate(uow, orderstate = OrderState.SHIP_READY)