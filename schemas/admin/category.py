from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., example="Snacks")
    image_url: Optional[str] = Field(None, example="uploaded_images/categories/abc123.png")
    building_id: str
    stall_id: str
    admin_id: Optional[str] = None
    manager_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    building_id: Optional[str] = None
    stall_id: Optional[str] = None
    admin_id: Optional[str] = None
    manager_id: Optional[str] = None


class CategoryOut(CategoryBase):
    id: str
    class Config:
        orm_mode = True
