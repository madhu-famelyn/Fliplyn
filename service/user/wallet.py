from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List, Dict
from datetime import datetime, timedelta, timezone, time

from models.user.order import Order
from models.user.wallet import Wallet
from models.user.user import User


def create_wallet_for_user(
    db: Session,
    user_id: str,
    wallet_amount: float,
    building_id: Optional[str] = None
) -> Wallet:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    if wallet:
        now_utc = datetime.now(timezone.utc)
        expiry_utc = wallet.expiry_at.astimezone(timezone.utc) if wallet.expiry_at else None

        if expiry_utc and now_utc > expiry_utc:
            wallet.wallet_amount = 0.0
            wallet.balance_amount = 0.0

        wallet.wallet_amount += wallet_amount
        wallet.balance_amount += wallet_amount
        wallet.expiry_at = expiry_time

        if building_id:
            wallet.building_id = building_id

        db.commit()
        db.refresh(wallet)
        return wallet

    new_wallet = Wallet(
        user_id=user_id,
        building_id=building_id,
        wallet_amount=wallet_amount,
        balance_amount=wallet_amount,
        expiry_at=expiry_time
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet


def get_wallet_by_user_id(db: Session, user_id: str) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    now_utc = datetime.now(timezone.utc)
    expiry_utc = wallet.expiry_at.astimezone(timezone.utc) if wallet.expiry_at else None

    if not wallet.is_retainable and expiry_utc and now_utc > expiry_utc:
        wallet.wallet_amount = 0.0
        wallet.balance_amount = 0.0
        db.commit()
        db.refresh(wallet)

    return wallet


def add_money_to_wallet(
    db: Session,
    identifier: str,
    wallet_amount: float,
    building_id: str,  # ✅ Required
    is_retainable: bool = False
) -> Wallet:
    if not building_id:
        raise HTTPException(status_code=400, detail="Building ID is required")

    user = db.query(User).filter(
        (User.phone_number == identifier) | (User.company_email == identifier)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expiry_time = None
    if not is_retainable:
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        expiry_time = datetime.combine(tomorrow.date(), time(0, 0, tzinfo=timezone.utc))

    wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()

    if wallet:
        now = datetime.now(timezone.utc)
        if not wallet.is_retainable and wallet.expiry_at and now > wallet.expiry_at:
            wallet.wallet_amount = 0.0
            wallet.balance_amount = 0.0

        wallet.wallet_amount += wallet_amount
        wallet.balance_amount += wallet_amount
        wallet.expiry_at = expiry_time
        wallet.is_retainable = is_retainable
        wallet.building_id = building_id  # ✅ Always update

        db.commit()
        db.refresh(wallet)
        return wallet

    new_wallet = Wallet(
        user_id=user.id,
        building_id=building_id,
        wallet_amount=wallet_amount,
        balance_amount=wallet_amount,
        expiry_at=expiry_time,
        is_retainable=is_retainable
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet


def get_wallet_transaction_history(user_id: str, db: Session) -> List[Dict]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = []

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if wallet:
        transactions.append({
            "date": wallet.created_datetime.isoformat(),
            "amount": float(wallet.wallet_amount)
        })

    orders = db.query(Order).filter(Order.user_id == user_id, Order.paid_with_wallet == True).all()
    for order in orders:
        transactions.append({
            "date": order.created_datetime.isoformat(),
            "amount": -float(order.total_amount)
        })

    transactions.sort(key=lambda x: x["date"], reverse=True)
    return transactions


def get_wallets_by_building_id(db: Session, building_id: str) -> List[Wallet]:
    wallets = db.query(Wallet).filter(Wallet.building_id == building_id).all()
    if not wallets:
        raise HTTPException(status_code=404, detail="No wallets found for this building")
    return wallets
