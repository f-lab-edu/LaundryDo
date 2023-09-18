from src.domain.spec import LAUNDRYBAG_MAXVOLUME, MACHINE_MAXVOLUME, LaundryTimeTable, time_required_for_volume
from .clothes import ClothesState
from .laundrybag import LaundryBag, LaundryBagState
from src.domain.base import Base

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Interval


from enum import Enum
from typing import List
from datetime import datetime, timedelta

class MaximumVolumeExceedError(Exception) :
    pass

class AlreadyRunningError(Exception) :
    pass

class BrokenError(Exception) :
    pass


class MachineState(str, Enum):
    READY = "준비"
    STOP = "정지"
    RUNNING = "세탁중"
    DONE = "세탁완료"  # 세탁 완료 후 laundryBag이 reclaim되어야 다시 '준비'상태로 돌아갈 수 있다.                                                                                                                                                                                                                                                                                                                                                                 꺼내야하는 상태
    BROKEN = "고장"


class Machine(Base):

    __tablename__ = 'machine'

    id =  Column('id', Integer, primary_key = True, autoincrement = True)
    machineid = Column('machineid', String(255), unique = True)
    contained = relationship('LaundryBag', backref = 'machine', uselist = False)
    runtime = Column('runtime', Interval, default = timedelta(0))
    start_at = Column('start_at', DateTime, nullable = True)
    update_at = Column('lastupdate_time', DateTime, default = datetime.now(), onupdate = datetime.now())
    status = Column('status', sqlalchemy.Enum(MachineState), default = MachineState.READY)

    def __init__(self, machineid: str):
        self.machineid = machineid
        self.contained = None  # LaundryBag

        self.start_at = None
        self._requiredTime = None
        self._label = None

        # 가장 첫번째 호출시에만 사용. DB에 등록되기 전
        self.status = MachineState.READY

        # TODO [Machine] sort by least recent used machine.
        # TODO [Machine] max volume may be different.
    
    def __gt__(self, other) :

        # sort 함수는 laundrybag을 allocate하기 전에만 사용한다. [STOP, DONE, BROKEN] 상태의 machine은 제외

        if not isinstance(other, self.__class__) :
            raise NotImplementedError()
        
        if self.status in [MachineState.STOP, MachineState.DONE, MachineState.BROKEN] :
            return True
        elif other.status in [MachineState.STOP, MachineState.DONE, MachineState.BROKEN] :
            return False

        

        elif self.status == MachineState.RUNNING and other.status == MachineState.RUNNING :
            exectime = datetime.now()
            own_remainingTime = self.requiredTime - ((exectime - self.update_at ) + self.runtime )
            other_remainingTime = other.requiredTime - ((exectime - other.update_at ) + other.runtime )
            return own_remainingTime > other_remainingTime
        elif self.status == MachineState.RUNNING and other.status != MachineState.RUNNING :
            return True
        elif other.status == MachineState.RUNNING and self.status != MachineState.RUNNING:
            return False
        elif self.status == MachineState.READY and other.status == MachineState.READY :
            return self.update_at > other.update_at

    @property
    def volume(self):
        if self.contained is None:
            return None
        return self.contained.volume

    @property
    def label(self):
        if self.contained is None:
            return None
        return self.contained.label

    @property
    def requiredTime(self):
        if self.label is None:
            return None
        self._requiredTime = time_required_for_volume(
            LaundryTimeTable[self.label], self.volume
        )
        return timedelta(minutes = self._requiredTime)

    
    def update_status(self) :
        if self.runtime >= self.requiredTime : # runtime이 requiredTime보다 더 커질 수도?
            self.status = MachineState.DONE
            self.contained.status = LaundryBagState.DONE
    
    def update_runtime(self) :
        if self.update_at and self.status == MachineState.RUNNING:
            self.runtime += (datetime.now() - self.update_at)
        elif self.status == MachineState.DONE :
            self.runtime = timedelta(0)
            self.contained.status = LaundryBagState.DONE
            

    def __hash__(self) :
        return hash(self.machineid)

    def __eq__(self, other) :
        return self.__hash__ == other.__hash__

    def can_contain(self, laundrybag: LaundryBag):
        return laundrybag.volume <= MACHINE_MAXVOLUME

    def start(self, laundrybag: LaundryBag):
        # TODO : [Machine] Broken Machine -> Move LaundryBags to other Machine
        # 세탁기기가 고장날 경우 처리방법
        if self.status == MachineState.BROKEN :
            raise BrokenError(f'{self.__repr__} is broken.')
        elif not self.can_contain(laundrybag):
            raise MaximumVolumeExceedError("cannot contain the bag, too large.")
        elif self.status == MachineState.RUNNING :
            raise AlreadyRunningError(f'Machine {self.id} is already running.')
        else :
            self.start_at = datetime.now()
            self.update_at = self.start_at
            self.runtime = timedelta(0)
            self.status = MachineState.RUNNING

            laundrybag.status = LaundryBagState.RUNNING
            self.contained = laundrybag
            for clothes in laundrybag.clothes_list :
                clothes.status = ClothesState.PROCESSING

    def resume(self):
        if self.status == MachineState.STOP:
            self.update_at = datetime.now()
            self.status = MachineState.RUNNING
        else:
            raise AlreadyRunningError(f"cannot resume when {self.status}")

    def stop(self):
        if self.status == MachineState.RUNNING:
            self.status = MachineState.STOP
            exec_time = datetime.now()

            self.runtime += exec_time - self.update_at
            self.update_at = exec_time
        else:
            raise ValueError(f"cannot stop when {self.status}")
        
    

    def __repr__(self) :
        return f'id={self.machineid}, contained={self.contained.laundrybagid if self.contained else None}, status={self.status}'