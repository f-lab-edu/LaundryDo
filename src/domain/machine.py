from .spec import LAUNDRYBAG_MAXVOLUME, MACHINE_MAXVOLUME, LaundryTimeTable, time_required_for_volume
from .clothes import ClothesState
from .laundrybag import LaundryBag, LaundryBagState


from enum import Enum
from typing import List
from datetime import datetime, timedelta



class MachineState(Enum):
    READY = "준비"
    STOP = "정지"
    RUNNING = "세탁중"
    DONE = "세탁완료"  # 세탁 완료 후 laundryBag이 reclaim되어야 다시 '준비'상태로 돌아갈 수 있다.                                                                                                                                                                                                                                                                                                                                                                 꺼내야하는 상태
    BROKEN = "고장"


class Machine:
    def __init__(self, machineid: str):
        self.machineid = machineid
        self.contained = None  # LaundryBag

        self.start_time = None
        self.lastupdateTime = None
        self.runtime = timedelta(minutes=0)

        self.status = MachineState.READY

        ## TODO : sort by least recent used machine.
        ## TODO : max volume may be different.

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

    def put(self, laundrybag: LaundryBag):
        ## TODO : if machine is broken for some time, then move laundrybags to other machine
        if self.can_contain(laundrybag) and self.status not in [MachineState.RUNNING, MachineState.BROKEN]:
            laundrybag.status = LaundryBagState.RUN
            self.contained = laundrybag
            
        else:
            raise ValueError("cannot contain the bag, too large.")

    def start(self, exec_time: datetime):
        if self.status == MachineState.RUNNING:
            raise ValueError("machine is already running")
        elif self.status == MachineState.BROKEN:
            raise ValueError("machine is broken.")

        if self.contained is None:
            raise ValueError("No LaundryBag in the Machine")

        self.start_time = exec_time
        self.lastupdateTime = self.start_time
        self.status = MachineState.RUNNING

    def resume(self, exec_time: datetime):
        if self.status == MachineState.STOP:
            self.lastupdateTime = exec_time
            self.status = MachineState.RUNNING
        else:
            raise ValueError(f"cannot resume when {self.status}")

    def stop(self, exec_time: datetime):
        if self.status == MachineState.RUNNING:
            self.status = MachineState.STOP
            # now = datetime.now()
            self.runtime += exec_time - self.lastupdateTime
            self.lastupdateTime = exec_time
        else:
            raise ValueError(f"cannot stop when {self.status}")