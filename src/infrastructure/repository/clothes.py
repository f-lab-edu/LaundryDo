
from src.domain.repository import ClothesRepository
from src.domain import Clothes, ClothesState
from typing import List

class MemoryClothesRepository(ClothesRepository) :
    
    def __init__(self, clothes_dict : dict = {}) :
        self._clothes_dict = clothes_dict

    def get(self, clothesid : str) -> Clothes :
        return self._clothes_dict.get(clothesid)

    def get_by_status(self, status : ClothesState) -> List[Clothes]  :
        return [clothes for clothes in self._clothes_dict.values() if clothes.status == status]

    def list(self) :
        return self._clothes_dict.values()
    
    def add(self, clothes : Clothes) :
        self._clothes_dict[clothes.clothesid] = clothes


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


