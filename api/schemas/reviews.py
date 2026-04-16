from typing import Optional
from pydantic import BaseModel

class ReviewBase(BaseModel):
    order_id: int
    score: int

class ReviewCreate(ReviewBase):
    review_text: Optional[str] = None

class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[int] = None

class Review(ReviewBase):
    id: int
    review_text: Optional[str] = None

    class ConfigDict:
        from_attributes = True