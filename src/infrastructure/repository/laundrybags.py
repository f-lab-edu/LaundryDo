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

    def list(self) :
        return list(self.session.query(LaundryBag).values())
    
    def add(self, laundrybag : LaundryBag) :
        self.session.buffers[LaundryBag][laundrybag.laundrybagid] = laundrybag



class SqlAlchemyLaundryBagRepository(AbstractLaundryBagRepository) : 
    
    def __init__(self, session) :
        self.session = session

    def get(self, laundrybagid : str) -> LaundryBag:
        return self.session.query(LaundryBag).filter_by(laundrybagid = laundrybagid).first()

    def get_by_status(self, status : LaundryBagState) -> list[LaundryBag] :
        return self.session.query(LaundryBag).filter_by(status = status).all()
    
    def get_by_status_and_label(self, status : LaundryBagState, label : LaundryLabel) -> LaundryBag :
        '''
        return a laundrybag that is LaundryBagState.COLLECTING and LaundryLabel
        '''
        waiting_bags_by_label = self.session.query(LaundryBag).filter_by(status = status).filter_by(label = label).all() #.order_by(LaundryBag.created_at)

        return waiting_bags_by_label                  

    def list(self) :
        return self.session.query(LaundryBag).all()
    
    def add(self, laundrybag : LaundryBag) :
        self.session.add(laundrybag)