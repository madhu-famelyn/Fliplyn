from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class WalletGroupCreate(BaseModel):
    group_name: str = Field(..., example="Marketing Team")
    building_id: str = Field(..., example="0f0e5c3a-3c9d-4c7f-8b8d-123456789abc")
    user_phone_numbers: List[str] = Field(..., example=["9876543210", "9876543211"])

class WalletGroupOut(BaseModel):
    id: str
    group_name: str
    building_id: str
    user_phone_numbers: List[Dict[str, str]]
    created_datetime: datetime

    class Config:
        orm_mode = True


class WalletGroupFundCreate(BaseModel):
    group_id: str = Field(..., example="wallet-group-uuid")
    wallet_amount: float = Field(..., gt=0, example=100.0)
    is_retainable: bool = Field(..., example=True)



class WalletGroupUpdate(BaseModel):
    group_name: Optional[str]
    user_phone_numbers: Optional[List[str]]

    class Config:
        orm_mode = True



class WalletOut(BaseModel):
    id: str
    user_id: str
    building_id: Optional[str]
    wallet_amount: float
    balance_amount: float
    expiry_at: Optional[datetime]
    is_retainable: bool
    created_datetime: Optional[datetime]
    updated_datetime: Optional[datetime]

    class Config:
        orm_mode = True



class WalletGroupUserAdd(BaseModel):
    group_id: str = Field(..., example="wallet-group-uuid")
    phone_number: str = Field(..., example="9876543210")


class WalletGroupUserRemove(BaseModel):
    group_id: str = Field(..., example="wallet-group-uuid")
    phone_number: str = Field(..., example="9876543210")