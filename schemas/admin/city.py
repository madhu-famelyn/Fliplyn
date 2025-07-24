from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# ✅ Base schema with shared attributes
class CityBase(BaseModel):
    city: str = Field(..., example="Chennai")


# ✅ For creating a new city entry
class CityCreate(CityBase):
    admin_id: UUID
    country_id: UUID
    state_id: UUID


# ✅ For updating an existing city (optional fields)
class CityUpdate(BaseModel):
    city: Optional[str] = Field(None, example="New Delhi")
    state_id: Optional[UUID]
    country_id: Optional[UUID]


# ✅ For returning data to clients
# ✅ For returning data to clients
class CityOut(CityBase):
    id: UUID
    admin_id: UUID
    country_id: UUID
    state_id: UUID
    city_id: str  # <- ✅ Add this line

    class Config:
        orm_mode = True
