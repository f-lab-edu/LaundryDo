from src.domain.repository import MachineRepository
from src.domain import Machine, MachineState
from typing import List


class MemoryMachineRepository(MachineRepository) :
    
    def __init__(self, machines : dict = {} ) :
        self._machines = {}

    def get(self, machineid : str) -> Machine :
        return self._machines.get(machineid)

    def get_by_status(self, status : MachineState) -> List[Machine] :
        return [machine for machine in self._machines.values() if machine.status == status]

    def list(self) :
        return self._machines.values()
    
    def add(self, machine : Machine) :
        self._machines[machine.machineid] = machine


class SqlAlchemyMachineRepository(MachineRepository) :
    
    def __init__(self, session) :
        self.session = session

    def get(self, machineid : str) -> Machine:
        return self.session.query(Machine).filter_by(machineid = machineid).one()

    def get_by_status(self, status : MachineState) -> List[Machine] :
        return self.session.query(Machine).filter_by(status = status).all()


    def list(self) :
        return self.session.query(Machine).all()
    
    def add(self, machine: Machine) :
        self.session.add(machine)
