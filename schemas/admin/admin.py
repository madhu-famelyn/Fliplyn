from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base schema for shared fields
class AdminBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

# For creating a new Admin
class AdminCreate(AdminBase):
    name: str
    email: EmailStr
    phone_number: str
    password: str  # This will later be hashed

# For updating an existing Admin
class AdminUpdate(AdminBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

# For reading Admin details (out schema)
class AdminOut(AdminBase):
    id: str
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True

# For deletion (can be used in route body or as param)
class AdminDelete(BaseModel):
    id: str


