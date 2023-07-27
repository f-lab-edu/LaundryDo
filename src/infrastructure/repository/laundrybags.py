from src.domain.repository import LaundryBagRepository
from src.dbmodel import LaundryBag, LaundryBagState, LaundryLabel
from typing import List

from uuid import uuid4
from datetime import datetime


class MemoryLaundryBagRepository(LaundryBagRepository) : 
    
    def __init__(self, laundrybags : dict = {}) :
        self._laundrybags = {laundrybag.laundrybagid : laundrybag for laundrybag in laundrybags}

    def get(self, laundrybagid : str) -> LaundryBag :
        return self._laundrybags.get(laundrybagid)

    def get_by_status(self, status : LaundryBagState) -> List[LaundryBag] :
        return [laundrybag for laundrybag in self._laundrybags.values() if laundrybag.status == status]

    def get_waitingbag_by_label(self, label : LaundryLabel) -> LaundryBag :
        '''
        get list of laundrybags that are LaundryBagState.READY and LaundryLabel
        '''
        return next((laundrybag for laundrybag in self._laundrybags.values() 
                    if laundrybag.status == LaundryBagState.COLLECTING and laundrybag.label == label), None)

    def list(self) :
        return self._laundrybags.values()
    
    def add(self, laundrybag : LaundryBag) :
        self._laundrybags[laundrybag.laundrybagid] = laundrybag


class SqlAlchemyLaundryBagRepository(LaundryBagRepository) : 
    
    def __init__(self, session) :
        self.session = session

    def get(self, laundrybagid : str) -> LaundryBag:
        return self.session.query(LaundryBag).filter_by(laundrybagid = laundrybagid).one()

    def get_by_status(self, status : LaundryBagState) -> list[LaundryBag] :
        return self.session.query(LaundryBag).filter_by(status = status).all()

    def get_waitingbag_by_label(self, label : LaundryLabel) -> LaundryBag :
        '''
        get list of laundrybags that are LaundryBagState.READY and LaundryLabel
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