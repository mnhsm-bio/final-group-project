from typing import Optional, List
from pydantic import BaseModel


class SandwichBase(BaseModel):
    sandwich_name: str
    price: float
    calories: Optional[int] = None
    food_category: Optional[str] = None


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[str] = None

class IngredientDetail(BaseModel):
    name: str
    amount: int

    class ConfigDict:
        from_attributes = True


class Sandwich(SandwichBase):
    id: int
    ingredients: Optional[List[IngredientDetail]] = []

    class ConfigDict:
        from_attributes = True