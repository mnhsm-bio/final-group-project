from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    tracking_number: Optional[str] = None
    order_status: Optional[str] = "pending"
    total_price: Optional[float] = None
    promo_code: Optional[str] = None
    discount_total: Optional[float] = None
    customer_id: Optional[int] = None
    order_type: Optional[str] = "takeout"


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    promo_code: Optional[str] = None
    discount_total: Optional[float] = None
    customer_id: Optional[int] = None
    order_type: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    promo_code: Optional[str] = None
    discount_total: Optional[float] = None
    customer_id: Optional[int] = None
    order_type: Optional[str] = None


    class ConfigDict:
        from_attributes = True