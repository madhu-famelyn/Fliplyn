from pydantic import BaseModel, Field
from typing import Optional


class StateCreate(BaseModel):
    vendor_id: str = Field(..., example="uuid-of-vendor")
    country_id: str = Field(..., example="uuid-of-country")
    state_name: str = Field(..., example="Tamil Nadu")  # Matches fixed list
    # ✅ No need to pass state_id manually, it will be auto-generated in backend


class StateUpdate(BaseModel):
    country_id: Optional[str] = Field(None, example="uuid-of-country")
    state_name: Optional[str] = Field(None, example="Kerala")
    # ❌ No state_id here — keep backend-controlled


class StateOut(BaseModel):
    id: str
    vendor_id: str
    country_id: str
    state_name: str
    state_id: str  # ✅ Include in output

    class Config:
        from_attributes = True  # Allows ORM → schema conversion

