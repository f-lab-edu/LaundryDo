
from src.domain.repository import ClothesRepository
from .session import FakeSession
from src.domain import Clothes, ClothesState
from typing import List

class MemoryClothesRepository(ClothesRepository) :
    
    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, clothesid : str) -> Clothes :
        return self.session.query(Clothes).get(clothesid)

    def get_by_status(self, status : ClothesState) -> List[Clothes]  :
        return self.session.query(Clothes).filter_by(status = status)

    def list(self) :
        return self.session.query(Clothes).values()
    
    def add(self, clothes : Clothes) :
        self.session.buffer[Clothes][clothes.clothesid] = clothes


class SqlAlchemyClothesRepository(ClothesRepository) :
    
    def __init__(self, session) :
        self.session = session

    def get(self, clothesid : str) -> Clothes :
        return self.session.query(Clothes).filter_by(clothesid = clothesid).one()

    def get_by_status(self, status : ClothesState) -> List[Clothes] :
        return self.session.query(Clothes).filter_by(status = status).all()

    def list(self) :
        return self.session.query(Clothes).all()
    
    def add(self, clothes : Clothes) :
        self.session.add(clothes)




