from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PromotionBase(BaseModel):
    promotion_code: str
    expiration_date: datetime
    discount_value: float


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None
    expiration_date: Optional[datetime] = None
    discount_value: Optional[float] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True