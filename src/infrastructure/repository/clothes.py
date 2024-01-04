
from src.domain.repository import AbstractClothesRepository
from .session import FakeSession
from src.domain import Clothes, ClothesState, LaundryLabel
from typing import List

class MemoryClothesRepository(AbstractClothesRepository) :
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, clothesid : str) -> Clothes :
        return self.session.query(Clothes).get(clothesid)

    def get_by_status(self, status : ClothesState) -> List[Clothes]  :
        return self.session.query(Clothes).filter_by(status = status)

    def get_by_status_and_label(self, status : ClothesState, label : LaundryLabel) -> List[Clothes] :
        raise NotImplemented

    def list(self) :
        return list(self.session.query(Clothes).values())
    
    def add(self, clothes : Clothes) :
        self.session.buffers[Clothes][clothes.clothesid] = clothes


class SqlAlchemyClothesRepository(AbstractClothesRepository) :
    
    def __init__(self, session) :
        self.session = session

    def get(self, clothesid : str) -> Clothes :
        return self.session.query(Clothes).filter_by(clothesid = clothesid).first()

    def get_by_status(self, status : ClothesState) -> List[Clothes] :
        return self.session.query(Clothes).filter_by(status = status).all()

    def get_by_status_and_label(self, status : ClothesState, label : LaundryLabel) -> List[Clothes] :
        return self.session.query(Clothes).filter_by(status = status).filter_by(label = label).all()

    def list(self) :
        return self.session.query(Clothes).all()
    
    def add(self, clothes : Clothes) :
        self.session.add(clothes)




