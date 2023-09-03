from src.domain.repository import AbstractMachineRepository
from .session import FakeSession
from src.domain import Machine, MachineState
from typing import List

## Machine set is less likely to be changed.

class MemoryMachineRepository(AbstractMachineRepository) :
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, machineid : str) -> Machine :
        return self.session.query(Machine).get(machineid)

    def get_by_status(self, status : MachineState) -> List[Machine] :
        return self.session.query(Machine).filter_by(status = status)

    def list(self) :
        return list(self.session.query(Machine).values())
    
    def add(self, machine : Machine) :
        self.session.query(Machine)[machine.machineid] = machine


class SqlAlchemyMachineRepository(AbstractMachineRepository) :
    
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
