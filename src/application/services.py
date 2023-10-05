from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRY_MINVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from src.domain.clothes import Clothes, ClothesState, LaundryLabel
from src.domain.order import Order, OrderState, clothes_order_mapping
from src.domain.laundrybag import LaundryBag, LaundryBagState
from src.domain.machine import Machine, MachineState
from src.domain.repository import AbstractOrderRepository, AbstractLaundryBagRepository, AbstractMachineRepository
from src.application.unit_of_work import AbstractUnitOfWork

from collections import deque
from typing import List, Dict
from datetime import datetime
from uuid import uuid4

from collections import deque, defaultdict




class OrderCannotbeCancelledError(Exception) :
    pass


def request_order(uow : AbstractUnitOfWork, orderid, userid, clothes_list, received_at) :
    with uow :
        uow.orders.add(Order(orderid = orderid,
                             userid = userid,
                             clothes_list = [Clothes(**dict(clothes)) for clothes in clothes_list], 
                             received_at = received_at))
        uow.commit()


def cancel_order(uow : AbstractUnitOfWork, userid : str, orderid : str) :
    with uow : 
        order = uow.orders.get_by_id(orderid = orderid)
        if order.status == OrderState.PREPARING :
            # cancel the order
            raise OrderCannotbeCancelledError
        uow.commit()
    return order


# order -> laundrybags process
# get waiting laundrybags
# sort order.clothes_list by label
# put in laundrybag if laundrybag can contain the clothes, else make new laundrybag

def update_orderstate(uow : AbstractUnitOfWork, orderstate : OrderState) :
    with uow :
        orders = uow.orders.get_by_status(status = orderstate)
        for order in orders :
            order.update_status()
            uow.orders.add(order)
        uow.commit()


def allocate_clothes_in_laundrybag(uow : AbstractUnitOfWork) -> None :
    with uow :
        for label in LaundryLabel.__members__ :
            clothes_list = uow.clothes.get_by_status_and_label(status = ClothesState.PREPARING, label = label)
            clothes_list = deque(clothes_list)
            while clothes_list :
                clothes = clothes_list.popleft()
                found = False
                laundrybag_list = uow.laundrybags.get_by_status_and_label(status = LaundryBagState.COLLECTING, label = label)
                
                for laundrybag in laundrybag_list :
                    if laundrybag.can_contain(clothes) : 
                        clothes.status = ClothesState.DISTRIBUTED
                        laundrybag.append(clothes)
                        found = True
                        break
                
                
                if not found :
                    new_bag = LaundryBag(laundrybagid = f'bag-{label}-{len(laundrybag_list)}')

                    clothes.status = ClothesState.DISTRIBUTED
                    new_bag.append(clothes)

                    uow.laundrybags.add(new_bag)
                
                uow.commit()





'''
with uow :
    waiting_orders = uow.orders.get_by_status(status = OrderState.PREPARING)
    laundrybags_in_collect = uow.laundrybags.get_by_status(status = LaundryBagState.COLLECTING)
    
    laundrybag_labeldict = defaultdict(list)
    for laundrybag in laundrybags_in_collect :
        laundrybag_labeldict[laundrybag.label] = laundrybag
    
    
    for order in waiting_orders :
        for clothes in order.clothes_list :
            

        order.status = max([clothes.status for clothes in order.clothes_list])
'''



def update_laundrybag_state(uow : AbstractUnitOfWork) :
    with uow :
        laundrybags_collecting = uow.laundrybags.get_by_status(status = LaundryBagState.COLLECTING)
        
        for laundrybag in laundrybags_collecting : 
            if laundrybag.created_at - datetime.now() >= LAUNDRYBAG_MAX_WAITINGTIME :
                laundrybag.status = LaundryBagState.READY



def distribute_order(order_list : List[Order]) -> Dict[LaundryLabel, List[Clothes]]:
    laundrylabeldict = {}

    for order in order_list:
        for clothes in order.clothes_list:
            if clothes.label in laundrylabeldict:
                laundrylabeldict[clothes.label].append(clothes)
            else:
                laundrylabeldict[clothes.label] = [clothes]

    return laundrylabeldict



def allocate_laundrybag_to_machine(uow : AbstractUnitOfWork) :
    '''put laundrybag into available machine 
        ready_laundrybag_list = get_laundrybags()
        while get_available_machine() := machine :
            machine.start( ready_laundrybag_list.pop(), exec_time )
    '''
    with uow :
        laundrybags_in_ready = deque(sorted(uow.laundrybags.get_by_status(status=LaundryBagState.READY)))
        print('1. put_laundrybag_into_machine')
        available_machines = deque(sorted(uow.machines.get_by_status(status = MachineState.READY)))
        
        print(f'available machines : {available_machines}')
        print(f'laundrybags in ready : {laundrybags_in_ready}')

        while available_machines and laundrybags_in_ready :
            print('matching laundrybag to machine...')
            machine = available_machines.popleft()
            laundrybag = laundrybags_in_ready.popleft()
            machine.start(laundrybag)
            uow.machines.add(machine)
        uow.commit()
    # update order state
    update_orderstate(uow, orderstate = OrderState.PREPARING)


###################
# Scheduling Jobs #
###################


def update_machine_state_if_laundry_done(uow : AbstractUnitOfWork) :
    '''
    update Machine(RUNNING), if the remainingTime == 0
    '''
    with uow : 
        machines_in_progress = uow.machines.get_by_status(status = MachineState.RUNNING)
        for machine in machines_in_progress :
            machine.update_runtime()
            machine.update_status()

            
            uow.machines.add(machine)

        uow.commit()

    update_orderstate(uow, orderstate = OrderState.WASHING)



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
    with uow :
        finished_machines = uow.machines.get_by_status(status = MachineState.DONE)
        print('2. reclaim_clothes_from_machine')
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

            uow.laundrybags.add(laundrybag)
            uow.machines.add(machine)
        uow.commit()
    update_orderstate(uow, orderstate = OrderState.RECLAIMING)



def ship_finished_order(uow : AbstractUnitOfWork) : 
    '''SHIP
    reclaimed_orders = get_order_reclaimed()
    for order in reclaimed_orders :
        order.ship() # change order status to SHIP_READY
    '''
    update_orderstate(uow, orderstate = OrderState.SHIP_READY)