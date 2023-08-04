from src.domain.repository import AbstractLaundryBagRepository
from src.domain import LaundryBag, LaundryBagState, LaundryLabel
from typing import List
from .session import FakeSession

from uuid import uuid4
from datetime import datetime


class MemoryLaundryBagRepository(AbstractLaundryBagRepository) : 
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, laundrybagid : str) -> LaundryBag :
        return self.session.query(LaundryBag).get(laundrybagid)

    def get_by_status(self, status : LaundryBagState) -> List[LaundryBag] :
        return self.session.query(LaundryBag).filter_by(status = status)

    def get_waitingbag_by_label(self, label : LaundryLabel) -> LaundryBag :
        waitingbag_by_label_list = self.session.query(LaundryBag).filter_by(status = LaundryBagState.COLLECTING).filter_by(label = label)
        if waitingbag_by_label_list :
            return waitingbag_by_label_list[0]
        return
        

    def list(self) :
        return list(self.session.query(LaundryBag).values())
    
    def add(self, laundrybag : LaundryBag) :
        self.session.buffers[LaundryBag][laundrybag.laundrybagid] = laundrybag



class SqlAlchemyLaundryBagRepository(AbstractLaundryBagRepository) : 
    
    def __init__(self, session) :
        self.session = session

    def get(self, laundrybagid : str) -> LaundryBag:
        return self.session.query(LaundryBag).filter_by(laundrybagid = laundrybagid).one()

    def get_by_status(self, status : LaundryBagState) -> list[LaundryBag] :
        return self.session.query(LaundryBag).filter_by(status = status).all()

    def get_waitingbag_by_label(self, label : LaundryLabel) -> LaundryBag :
        '''
        return a laundrybag that is LaundryBagState.COLLECTING and LaundryLabel
        '''
        waiting_list = self.session.query(LaundryBag).filter_by(status = LaundryBagState.COLLECTING).all()

        waiting_bag_by_label = [bag for bag in waiting_list if bag.label == label]
        if not waiting_bag_by_label :
            waiting_bag_by_label = LaundryBag(laundrybagid=f'bag-{label}-{str(uuid4())[:2]}-0', created_at = datetime.now())
        else :
            waiting_bag_by_label = waiting_bag_by_label[0]

        return waiting_bag_by_label                  

    def list(self) :
        return self.session.query(LaundryBag).all()
    
    def add(self, laundrybag : LaundryBag) :
        self.session.add(laundrybag)