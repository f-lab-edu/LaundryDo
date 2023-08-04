from .spec import LAUNDRYBAG_MAXVOLUME, MACHINE_MAXVOLUME, LaundryTimeTable, time_required_for_volume
from .clothes import ClothesState
from .laundrybag import LaundryBag, LaundryBagState
from .base import Base

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime


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

    # id =  Column('id', Integer, primary_key = True, autoincrement = True)
    machineid = Column('machineid', String(255), primary_key = True)
    contained = relationship('LaundryBag', backref = 'machine', uselist = False)
    # Column('laundrybagid', ForeignKey('laundrybag.id')),
    start_time = Column('start_time', DateTime, nullable = True)
    lastupdateTime = Column('lastupdate_time', DateTime)
    status = Column('status', sqlalchemy.Enum(MachineState), default = MachineState.READY)

    def __init__(self, machineid: str):
        self.machineid = machineid
        self.contained = None  # LaundryBag

        self.start_time = None
        self.lastupdateTime = None
        self.runtime = timedelta(minutes=0)

        self.status = MachineState.READY

        # TODO [Machine] sort by least recent used machine.
        # TODO [Machine] max volume may be different.
    
    def __eq__(self, other) :
        return hash(self.machineid) == hash(other.machineid)

    def __gt__(self, other) :
        if not isinstance(other, self.__class__) :
            raise NotImplementedError()
        if self.status is MachineState.RUNNING and other.status is MachineState.RUNNING :
            return self.remainingTime(datetime.now()) > other.remainingTime(datetime.now())
        elif self.status is MachineState.RUNNING :
            return True
        elif other.status is MachineState.RUNNING :
            return False
        if self.lastupdateTime and other.lastupdateTime :
            return self.lastupdateTime > other.lastupdateTime

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
        return time_required_for_volume(
            LaundryTimeTable[self.label], self.volume
        )

    def get_runtime(self, exec_time: datetime):

        if self.lastupdateTime and self.status == MachineState.RUNNING:
            return self.runtime + (exec_time - self.lastupdateTime)
        else:
            return self.runtime
    
    def remainingTime(self, exec_time: datetime):
        return timedelta(minutes=self.requiredTime) - self.get_runtime(exec_time)

    def can_contain(self, laundryBag: LaundryBag):
        return laundryBag.volume <= MACHINE_MAXVOLUME

    def start(self, laundrybag: LaundryBag, exec_time):
        # TODO : [Machine] Broken Machine -> Move LaundryBags to other Machine
        # 세탁기기가 고장날 경우 처리방법
        if self.status == MachineState.BROKEN :
            raise BrokenError(f'{self.__repr__} is broken.')
        elif not self.can_contain(laundrybag):
            raise MaximumVolumeExceedError("cannot contain the bag, too large.")
        elif self.status == MachineState.RUNNING :
            raise AlreadyRunningError(f'{self.__repr__} is already running.')
        else :
            self.start_time = exec_time
            self.lastupdateTime = self.start_time
            self.status = MachineState.RUNNING

            laundrybag.status = LaundryBagState.RUNNING
            self.contained = laundrybag
            for clothes in laundrybag.clothes_list :
                clothes.status = ClothesState.PROCESSING

    # def start(self, exec_time: datetime):
    #     if self.status == MachineState.RUNNING:
    #         raise ValueError("machine is already running")
    #     elif self.status == MachineState.BROKEN:
    #         raise ValueError("machine is broken.")

    #     if self.contained is None:
    #         raise ValueError("No LaundryBag in the Machine")

    #     self.start_time = exec_time
    #     self.lastupdateTime = self.start_time
    #     self.status = MachineState.RUNNING

    def resume(self, exec_time: datetime):
        if self.status == MachineState.STOP:
            self.lastupdateTime = exec_time
            self.status = MachineState.RUNNING
        else:
            raise AlreadyRunningError(f"cannot resume when {self.status}")

    def stop(self, exec_time: datetime):
        if self.status == MachineState.RUNNING:
            self.status = MachineState.STOP
            # now = datetime.now()
            self.runtime += exec_time - self.lastupdateTime
            self.lastupdateTime = exec_time
        else:
            raise ValueError(f"cannot stop when {self.status}")
        
    

    def __repr__(self) :
        return f'id={self.machineid}, contained={self.contained.laundrybagid if self.contained else None}, status={self.status}'