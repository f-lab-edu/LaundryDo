from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRY_MINVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from src.domain.clothes import Clothes, ClothesState, LaundryLabel
from src.domain.order import Order, OrderState, clothes_order_mapping
from src.domain.laundrybag import LaundryBag, LaundryBagState
from src.domain.machine import Machine, MachineState
from src.domain.repository import AbstractOrderRepository, AbstractLaundryBagRepository, AbstractMachineRepository
from src.application.unit_of_work import AbstractUnitOfWork

from typing import List, Dict
from datetime import datetime
from uuid import uuid4

from collections import deque, defaultdict

class OrderCannotbeCancelledError(Exception) :
    pass


def request_order(uow : AbstractUnitOfWork, userid, clothes_list, received_at) :
    with uow :
        uow.orders.add(Order(userid = userid,
                             clothes_list = [Clothes(**dict(clothes)) for clothes in clothes_list], 
                             received_at = received_at))
        uow.commit()


def cancel_order(uow : AbstractUnitOfWork, userid : str, orderid : str) :
    with uow : 
        order = uow.orders.get_by_id(orderid = orderid)
        if order.status in [OrderState.SENDING, OrderState.PREPARING] :
            # cancel the order
            raise OrderCannotbeCancelledError
        uow.commit()
    return order


# order -> laundrybags process
# get waiting laundrybags
# sort order.clothes_list by label
# put in laundrybag if laundrybag can contain the clothes, else make new laundrybag


def update_orderstate(uow : AbstractUnitOfWork) :
    with uow : 
        orders = uow.orders.list()

        for order in orders :
            clothesstate = max(clothes.status for clothes in order.clothes_list)
            orderstate = clothes_order_mapping(clothesstate)
            order.status = orderstate
            uow.orders.add(order)
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



def change_laundrybagstate_if_time_passed(uow : AbstractUnitOfWork) :
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


def put_clothes_in_laundrybag(laundrybag : LaundryBag, clothes : Clothes) -> LaundryBag:
    laundrybaglist = []
    if laundrybag.can_contain(clothes.volume) :
        laundrybag.append(clothes)
        if laundrybag.volume == LAUNDRYBAG_MAXVOLUME :
            laundrybag.status = LaundryBagState.READY
    else :
        # 더 이상 clothes를 담지 못한다면, 세탁기로 이동하기 위한 상태로 변경
        laundrybag.status = LaundryBagState.READY
        laundrybaglist.append(laundrybag)
        laundrybag = LaundryBag(
                        laundrybagid = f'bag-{clothes.label}-{str(uuid4())[:2]}-{int(laundrybag.laundrybagid.split("-")[-1]) + 1}',
                        clothes_list = [clothes],
                        created_at = datetime.now()
                        )
    laundrybaglist.append(laundrybag)

    return laundrybaglist


    
def allocate_laundrybag(uow : AbstractUnitOfWork) :
    with uow :
        laundrylabeldict = distribute_order(uow.orders.get_by_status(status = OrderState.SENDING))

        for laundrylabel, clothes_list in laundrylabeldict.items() :
            waiting_bag = uow.laundrybags.get_waitingbag_by_label(label = laundrylabel)
            
            for clothes in clothes_list :
                waiting_bags = put_clothes_in_laundrybag(waiting_bag, clothes)
                for bag in waiting_bags :
                    uow.laundrybags.add(bag)

        uow.commit() 



###################
# Scheduling Jobs #
###################

def put_laundrybag_into_machine(uow : AbstractUnitOfWork) :
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
            machine.start(laundrybag, datetime.now())
            uow.machines.add(machine)
        uow.commit()


def update_machine_state_if_laundry_done(uow : AbstractUnitOfWork, exec_time : datetime) :
    '''
    update Machine(RUNNING), if the remainingTime == 0
    '''
    with uow : 
        machines_in_progress = uow.machines.get_by_status(status = MachineState.RUNNING)
        for machine in machines_in_progress :
            if machine.remainingTime == 0 :
                machine.status = MachineState.DONE
                uow.machines.add(machine)
                print(f'{machine} finished laundry.')

        uow.commit()



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
            machine.status = MachineState.READY
            uow.machines.add(machine)
        uow.commit()



def reclaim_clothes_into_order(uow : AbstractUnitOfWork):

    with uow :

        finished_laundrybags = uow.laundrybags.get_by_status(status = LaundryBagState.DONE)

        for laundryBag in finished_laundrybags:
            for clothes in laundryBag.clothes_list:
                clothes.status = ClothesState.RECLAIMED
                # if clothes.ordㅇerid not in reclaimed_dict:
                #     reclaimed_dict[clothes.orderid] = [clothes]
                # else:
                #     reclaimed_dict[clothes.orderid].append(clothes)
                uow.clothes.add(clothes)
            laundryBag.status = LaundryBagState.OBSOLETE
            uow.laundrybags.add(laundryBag)
        uow.commit()


def get_clothes_in_process(order: Order) -> List[Clothes]:
    '''
    Before shipping, check which clothes is not yet reclaimed.
    '''
    clothes_in_process = []

    for clothes in order.clothes_list:
        if clothes.status != ClothesState.RECLAIMED:
            clothes_in_process.append(clothes)
    return clothes_in_process


# def allocate(uow : AbstractUnitOfWork, laundrybag : LaundryBag) :

#     with uow :
#         available_machines = uow.machines.get_by_status(status = MachineState.READY)
        
#         try :
#             machine = next(available_machines)

#             machine.start(laundrybag, datetime.now())
#             uow.commit()
#         except StopIteration :
#             print('No available Machine right now. Putting laundrybag in waiting list')    
#             # TODO : [LaundryBag -> Machine]
#             # how to monitor laundrybag that was not able to be allocated at once.

def update_orderstate_fully_reclaimed(uow : AbstractUnitOfWork) : 
    '''UPDATE ORDER STATE 
    if 
    '''
    with uow : 
        orders_in_reclaiming = uow.orders.get_by_status(status = OrderState.RECLAIMING)
        print('3. check_order_is_fully_reclaimed')
        for order in orders_in_reclaiming :
            if not get_clothes_in_process(order) :
                order.status = OrderState.SHIP_READY
                uow.orders.add(order)
        uow.commit()
    

def ship(uow : AbstractUnitOfWork) : 
    '''SHIP
    reclaimed_orders = get_order_reclaimed()
    for order in reclaimed_orders :
        order.ship() # change order status to SHIP_READY
    '''
    with uow :
        orders_in_reclaiming = uow.orders.get_by_status(status = OrderState.SHIP_READY)
        print('4. ship')
    # if get_clothes_in_process(order) is None and order.status == OrderState.SHIP_READY :
        
    #     with uow :
        for order in orders_in_reclaiming :
            order.status = OrderState.SHIPPING
            uow.orders.add(order)
        uow.commit()