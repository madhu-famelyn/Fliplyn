from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db.session import get_db
from service.user.wallet import (
    create_wallet_for_user,
    get_wallet_by_user_id,
    add_money_to_wallet,
    get_wallet_transaction_history,
    get_wallets_by_building_id  # ✅ Import the new service
)
from schemas.user.wallet import WalletCreate, WalletOut, WalletAddMoney,  WalletFullOut 
from typing import List, Dict

wallet_routers = APIRouter(prefix="/wallets", tags=["Wallet"])

@wallet_routers.post("/", response_model=WalletOut)
def create_wallet(payload: WalletCreate, db: Session = Depends(get_db)):
    return create_wallet_for_user(
        db=db,
        user_id=payload.user_id,
        wallet_amount=payload.wallet_amount
    )


@wallet_routers .get("/{user_id}", response_model=WalletOut)
def get_wallet(user_id: str, db: Session = Depends(get_db)):
    return get_wallet_by_user_id(db=db, user_id=user_id)


@wallet_routers.post("/add-money", response_model=WalletOut)
def add_money(payload: WalletAddMoney, db: Session = Depends(get_db)):
    return add_money_to_wallet(
        db=db,
        identifier=payload.identifier,
        wallet_amount=payload.wallet_amount,
        building_id=payload.building_id, 
        is_retainable=payload.is_retainable
    )

@wallet_routers.get("/{user_id}/history", response_model=List[Dict])
def get_transaction_history(user_id: str, db: Session = Depends(get_db)):
    return get_wallet_transaction_history(user_id=user_id, db=db)

@wallet_routers.get("/by-building/{building_id}", response_model=List[WalletFullOut])
def get_wallets_by_building(building_id: str, db: Session = Depends(get_db)):
    return get_wallets_by_building_id(db=db, building_id=building_id)