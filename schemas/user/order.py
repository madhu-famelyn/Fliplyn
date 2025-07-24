from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# 🛒 Item in the order request
class OrderItem(BaseModel):
    item_id: str
    quantity: int


# 📥 Request payload for creating an order
class OrderCreate(BaseModel):
    user_id: str
    user_phone: str
    user_email: str
    items: List[OrderItem]
    pay_with_wallet: bool = Field(default=False)


# 📤 Item details in the response
class OrderItemDetail(BaseModel):
    item_id: str
    name: str
    description: str
    price: float
    quantity: int
    total: float


# 📤 Final response schema for the order
class OrderOut(BaseModel):
    id: str
    user_id: str
    user_phone: str
    user_email: str
    order_details: List[OrderItemDetail]  # ✅ Corrected to List
    total_amount: float
    paid_with_wallet: bool
    created_datetime: datetime

    class Config:
        orm_mode = True



class OrderItemOut(BaseModel):
    item_id: str
    name: str
    description: Optional[str]
    price: float
    quantity: int
    total: float
    stall_id: Optional[str]
    stall_name: Optional[str]
    stall_image_url: Optional[str]

class OrderDetailedOut(BaseModel):
    id: str
    user_id: str
    user_phone: str
    user_email: str
    order_details: List[OrderItemOut]
    total_amount: float
    paid_with_wallet: bool
    created_datetime: datetime

    class Config:
        orm_mode = True