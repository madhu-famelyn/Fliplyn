from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class StallBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    building_id: UUID
    admin_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None


class StallCreate(StallBase):
    pass


class StallUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    admin_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None


class StallOut(StallBase):
    id: UUID
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
