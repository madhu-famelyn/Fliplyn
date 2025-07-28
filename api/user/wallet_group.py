from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from config.db.session import get_db
from schemas.user.wallet_group import WalletGroupCreate, WalletGroupOut, WalletOut, WalletGroupFundCreate, WalletGroupUpdate,  WalletGroupUserAdd, WalletGroupUserRemove, WalletGroupOut
from service.user.wallet_group import create_wallet_group, fund_wallets_in_group, get_wallets_by_building_id, get_wallets_by_group_id, update_wallet_group

wallet_router = APIRouter(
    prefix="/wallet-group",
    tags=["Wallet Group"]
)

@wallet_router.post("/", response_model=WalletGroupOut)
def create_group(group_data: WalletGroupCreate, db: Session = Depends(get_db)):
    try:
        group = create_wallet_group(db=db, group_data=group_data)
        return group
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@wallet_router.post("/fund", response_model=List[WalletOut])
def fund_wallet_group(
    fund_data: WalletGroupFundCreate,
    db: Session = Depends(get_db)
):
    return fund_wallets_in_group(db, fund_data)



@wallet_router.get("/by-building/{building_id}")
def get_wallets(building_id: str, db: Session = Depends(get_db)):
    return get_wallets_by_building_id(db, building_id)




@wallet_router.get("/by-group/{group_id}")
def get_wallets_by_group(group_id: str, db: Session = Depends(get_db)):
    try:
        return get_wallets_by_group_id(db, group_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")




@wallet_router.put("/{group_id}", response_model=WalletGroupOut)
def update_group(group_id: str, update_data: WalletGroupUpdate, db: Session = Depends(get_db)):
    try:
        return update_wallet_group(db=db, group_id=group_id, update_data=update_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@wallet_router.post("/add-user", response_model=WalletGroupOut)
def add_user_to_group(data: WalletGroupUserAdd, db: Session = Depends(get_db)):
    return add_user_to_wallet_group(db, data)


@wallet_router.post("/remove-user", response_model=WalletGroupOut)
def remove_user_from_group(data: WalletGroupUserRemove, db: Session = Depends(get_db)):
    return remove_user_from_wallet_group(db, data)