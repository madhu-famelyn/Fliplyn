from pydantic import BaseModel
from typing import List, Optional


# ✅ Existing Schemas
class CartItemCreate(BaseModel):
    user_id: str
    item_id: str
    quantity: int


class BulkCartItemInput(BaseModel):
    item_id: str
    quantity: int


class CartBulkAddRequest(BaseModel):
    user_id: str
    items: List[BulkCartItemInput]


class CartItemOut(BaseModel):
    id: str
    item_id: str
    quantity: int
    price_at_addition: Optional[float]

    class Config:
        orm_mode = True


class CartCreate(BaseModel):
    user_id: str
    stall_id: str


class CartOut(BaseModel):
    id: str
    user_id: str
    stall_id: str
    items: List[CartItemOut]

    class Config:
        orm_mode = True


# ✅ New: For updating quantity of an item in cart
class CartItemUpdate(BaseModel):
    user_id: str
    item_id: str
    quantity: int  # set this to new quantity

# ✅ New: For removing an item from cart
class CartItemRemove(BaseModel):
    user_id: str
    item_id: str
