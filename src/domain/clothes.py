from enum import Enum
from datetime import datetime

class ClothesState(Enum):
    CANCELLED = "취소"
    PREPARING = "준비중"
    DISTRIBUTED = "세탁전분류"  # 세탁 라벨에 따라 분류된 상태
    PROCESSING = "세탁중"
    STOPPED = "일시정지"  # 세탁기 고장이나 외부 요인으로 세탁 일시 중지
    DONE = "세탁완료"
    RECLAIMED = "세탁후분류"

class LaundryLabel(Enum):
    WASH = "물세탁"
    DRY = "드라이클리닝"
    HAND = "손세탁"

class Clothes:
    def __init__(
        self,
        id: str,
        label: LaundryLabel,
        volume: float,
        orderid: str = None,
        status: ClothesState = ClothesState.PREPARING,
        received_at: datetime = None,
    ):
        self.id = id
        self.label = label
        self.volume = volume
        self.orderid = orderid
        self.status = status
        self.received_at = received_at

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.received_at < other.received_at
        else:
            raise TypeError(f"{type(other)} cannot be compared with Clothes class.")
