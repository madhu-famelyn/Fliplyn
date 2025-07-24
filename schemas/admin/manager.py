from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# ✅ Base schema used for shared attributes
class ManagerBase(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone_number: str = Field(..., example="9876543210")


# ✅ Schema used for manager creation
class ManagerCreate(ManagerBase):
    admin_id: str = Field(..., example="uuid-of-admin")
    building_id: str = Field(..., example="uuid-of-building")
    password: str = Field(..., min_length=6, example="securePassword123")

class ManagerUser(BaseModel):
    id: str
    email: EmailStr

class ManagerToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: ManagerUser


# ✅ Schema used for manager update
class ManagerUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Name")
    email: Optional[EmailStr] = Field(None, example="updated@example.com")
    phone_number: Optional[str] = Field(None, example="9999999999")
    password: Optional[str] = Field(None, min_length=6, example="newSecurePass456")


class ManagerLogin(BaseModel):
    email: EmailStr
    password: str


class ManagerToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict  # 👈 or use a proper Pydantic model if preferred

# ✅ Output schema for response serialization
class ManagerOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone_number: str
    admin_id: str
    building_id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
