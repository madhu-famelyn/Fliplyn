from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WalletCreate(BaseModel):
    user_id: str
    wallet_amount: float
    building_id: str  # ✅ Now required

class WalletAddMoney(BaseModel):
    identifier: str
    wallet_amount: float
    is_retainable: bool = False
    building_id: str  # ✅ Now required

class WalletOut(BaseModel):
    id: str
    user_id: str
    wallet_amount: float
    balance_amount: float
    building_id: Optional[str] = None 
    expiry_at: Optional[datetime]
    is_retainable: Optional[bool] = False
    created_datetime: datetime
    updated_datetime: Optional[datetime]

    class Config:
        orm_mode = True
class WalletFullOut(BaseModel):
    id: str
    user_id: str
    wallet_amount: float
    balance_amount: float
    expiry_at: Optional[datetime]
    is_retainable: Optional[bool] = False
    building_id: Optional[str] = None   
    created_datetime: datetime
    updated_datetime: Optional[datetime]

    class Config:
        orm_mode = True
