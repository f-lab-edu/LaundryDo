from src.domain import LaundryBag, LaundryBagState, LaundryLabel, Clothes
from src.application.unit_of_work import AbstractUnitOfWork
from src.domain.spec import LAUNDRYBAG_MAXVOLUME, LAUNDRYBAG_MAX_WAITINGTIME
from typing import List
from collections import defaultdict
from datetime import datetime
from uuid import uuid4

'''
repository에서 대기 중인 laundrybag을 불러옴
laundrybag에 order.clothes_list를 label별로 할당함
'''

class ClothesMaxVolumeExceedError(Exception) :
    pass


## order state
## clothes state


class LaundryBagManager :
    def __init__(self, uow : AbstractUnitOfWork) :
        self.uow = uow
        with self.uow :
            waiting_landrybaglist = uow.laundrybags.get_by_status(status = LaundryBagState.COLLECTING)

        self.waiting_laundrybaglist = waiting_landrybaglist
        self.laundrybagdict = {label : None for label in LaundryLabel} # suppose there is always only one bag for each label.

        # classify laundrybag by laundrylabel in dictionary
        for laundrybag in self.waiting_laundrybaglist :
            self.laundrybagdict[laundrybag.label] = laundrybag



    def update_bagstate(self) :
        '''
        if self.current_laundrybag is READY. 
        READY condition : [volume == LAUNDRYBAG_MAXVOLUME or create_time - datetime.now() >= LAUNDRYBAG_MAX_WAITINGTIME]
        '''
    
        for laundrybag in self.laundrybagdict.values() :
            if laundrybag.volume == LAUNDRYBAG_MAXVOLUME or \
              laundrybag.create_at - datetime.now() >= LAUNDRYBAG_MAX_WAITINGTIME :
                
                laundrybag.status = LaundryBagState.READY
                new_bag = self.create_new_laundrybag(laundrybag.label)

                with self.uow :
                    self.uow.laundrybags.add(new_bag)
                    self.uow.commit()

                self.laundrybagdict[laundrybag.label] = new_bag

            with self.uow :
                self.uow.laundrybags.add(laundrybag)
                self.uow.commit()




    def allocate(self, clothes : Clothes) :
        laundrybag = self.laundrybagdict[clothes.label]

        if laundrybag and laundrybag.can_contain(clothes.volume) :
            laundrybag.append(clothes)
        else :
            # 만약 clothes 자체가 최대 수용 부피를 초과한다면
            if clothes.volume > LAUNDRYBAG_MAXVOLUME :
                raise ClothesMaxVolumeExceedError()
            
            laundrybag = self.create_new_laundrybag(label = clothes.label)
            
            laundrybag.append(clothes)

            ###
            self.laundrybagdict[clothes.label] = laundrybag

        with self.uow :
            # if self.laundrybagdict[clothes.label] :
            self.uow.laundrybags.add(self.laundrybagdict[clothes.label])


    def create_new_laundrybag(self, label : LaundryLabel) :
        prev_laundrybag = self.laundrybagdict[label]

        laundrybagid = f'bag-{label}-{str(uuid4())[:2]}-{int(prev_laundrybag.laundrybagid.split("-")[-1]) + 1}' if prev_laundrybag \
                            else f'bag-{label}-{str(uuid4())[:2]}-0'

        return LaundryBag(laundrybagid = laundrybagid,
                          created_at = datetime.now(),)
                        #   label = label)
        