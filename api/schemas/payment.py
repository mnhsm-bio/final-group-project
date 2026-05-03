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
    transaction_status: Optional[str] = None

class Payment(PaymentBase):
    card_id: Optional[str] = None
    transaction_status: Optional[str] = "pending"

    class ConfigDict:
        from_attributes = True

class PaymentWithTotal(PaymentBase):
    card_id: Optional[str] = None
    transaction_status: Optional[str] = "pending"
    total_price: Optional[float] = None

    class ConfigDict:
        from_attributes = True