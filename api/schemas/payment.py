from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    payment_type: str

class PaymentCreate(PaymentBase):
    card_id: Optional[str] = None
    transaction_status: Optional[str] = "pending"

class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    card_id: Optional[str] = None
    transaction_status: Optional[str] = "pending"

class Payment(PaymentBase):
    id: int
    card_id: Optional[str] = None
    transaction_status: Optional[str] = "pending"

    class ConfigDict:
        from_attributes = True