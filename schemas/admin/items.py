from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

# Shared fields for response
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None  # Changed from HttpUrl to str
    price: float
    tax_included: bool = False
    Gst_precentage: Optional[float] = 0.0
    is_available: bool = True  # ✅ Added here

# For item creation (incoming data)
class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    tax_included: bool
    Gst_precentage: float
    final_price: float = 0  # Will be calculated server-side
    is_available: bool = True  # ✅ Added here

    admin_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    building_id: UUID
    stall_id: UUID
    category_id: UUID

    @field_validator("admin_id", "manager_id", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        return None if v == "" else v

    @model_validator(mode="after")
    def check_admin_or_manager(self):
        if not self.admin_id and not self.manager_id:
            raise ValueError("Either admin_id or manager_id must be provided.")
        return self

# For updating item fields
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    tax_included: Optional[bool] = None
    Gst_precentage: Optional[float] = None
    final_price: Optional[float] = None
    is_available: Optional[bool] = None  # ✅ Added here

    admin_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    building_id: Optional[UUID] = None
    stall_id: Optional[UUID] = None
    category_id: Optional[UUID] = None

    @field_validator("admin_id", "manager_id", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        return None if v == "" else v

    @model_validator(mode="after")
    def check_admin_or_manager(self):
        if self.admin_id is None and self.manager_id is None:
            raise ValueError("Either admin_id or manager_id must be provided.")
        return self

class ItemAvailabilityUpdate(BaseModel):
    is_available: bool

# For item reading / returning response
class ItemOut(ItemBase):
    id: UUID
    final_price: float
    building_id: UUID
    stall_id: UUID
    category_id: UUID
    admin_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    created_datetime: datetime
    updated_datetime: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v2
    }
