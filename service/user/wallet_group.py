from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from models.user.wallet_group import WalletGroup
from models.user.user import User
from models.user.wallet import Wallet
from schemas.user.wallet_group import WalletGroupCreate, WalletGroupFundCreate, WalletGroupUpdate, WalletGroupUserAdd, WalletGroupUserRemove
from typing import List, Dict



def create_wallet_group(db: Session, group_data: WalletGroupCreate) -> WalletGroup:
    # ✅ Fetch all users using phone numbers
    users = db.query(User).filter(User.phone_number.in_(group_data.user_phone_numbers)).all()

    # ✅ Validate all phone numbers found
    found_phone_numbers = {user.phone_number for user in users}
    missing_numbers = set(group_data.user_phone_numbers) - found_phone_numbers
    if missing_numbers:
        raise HTTPException(
            status_code=404,
            detail=f"Users with phone numbers not found: {', '.join(missing_numbers)}"
        )

    # ✅ Prepare user detail objects
    user_info_list: List[Dict[str, str]] = [
        {
            "id": user.id,
            "phone_number": user.phone_number,
            "email": user.company_email  # or use user.email if applicable
        }
        for user in users
    ]

    # ✅ Create WalletGroup instance
    wallet_group = WalletGroup(
        group_name=group_data.group_name,
        building_id=group_data.building_id,
        user_phone_numbers=user_info_list  # list of dicts, stored as JSON in DB
    )

    db.add(wallet_group)
    db.commit()
    db.refresh(wallet_group)

    return wallet_group





def fund_wallets_in_group(db: Session, fund_data: WalletGroupFundCreate):
    # Get the wallet group
    wallet_group = db.query(WalletGroup).filter(WalletGroup.id == fund_data.group_id).first()
    if not wallet_group:
        raise HTTPException(status_code=404, detail="Wallet group not found")

    # Extract only phone numbers from the wallet_group
    phone_numbers = [entry["phone_number"] for entry in wallet_group.user_phone_numbers if "phone_number" in entry]

    # Get users from phone numbers
    users = db.query(User).filter(User.phone_number.in_(phone_numbers)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found for this wallet group")

    updated_wallets = []

    for user in users:
        wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
        expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)

        if wallet:
            # Expiry check
            now_utc = datetime.now(timezone.utc)
            expiry_utc = wallet.expiry_at.astimezone(timezone.utc) if wallet.expiry_at else None

            if expiry_utc and now_utc > expiry_utc:
                wallet.wallet_amount = 0.0
                wallet.balance_amount = 0.0

            wallet.wallet_amount += fund_data.wallet_amount
            wallet.balance_amount += fund_data.wallet_amount
            wallet.expiry_at = expiry_time
            wallet.is_retainable = fund_data.is_retainable

        else:
            wallet = Wallet(
                user_id=user.id,
                building_id=wallet_group.building_id,
                wallet_amount=fund_data.wallet_amount,
                balance_amount=fund_data.wallet_amount,
                expiry_at=expiry_time,
                is_retainable=fund_data.is_retainable
            )
            db.add(wallet)

        updated_wallets.append(wallet)

    db.commit()

    for wallet in updated_wallets:
        db.refresh(wallet)

    return updated_wallets




def get_wallets_by_building_id(db: Session, building_id: str) -> List[dict]:
    wallets = (
        db.query(Wallet)
        .join(User, Wallet.user_id == User.id)
        .filter(Wallet.building_id == building_id)
        .all()
    )

    if not wallets:
        raise HTTPException(status_code=404, detail="No wallets found for this building")

    result = []
    for wallet in wallets:
        result.append({
            "wallet_id": wallet.id,
            "user_id": wallet.user_id,
            "user_name": wallet.user.full_name if hasattr(wallet.user, "full_name") else None,
            "phone_number": wallet.user.phone_number,
            "email": wallet.user.company_email,
            "wallet_amount": wallet.wallet_amount,
            "balance_amount": wallet.balance_amount,
            "expiry_at": wallet.expiry_at,
            "is_retainable": wallet.is_retainable,
        })

    return result







def get_wallets_by_group_id(db: Session, group_id: str) -> List[Dict]:
    wallet_group = db.query(WalletGroup).filter(WalletGroup.id == group_id).first()
    if not wallet_group:
        raise HTTPException(status_code=404, detail="Wallet group not found")

    phone_numbers = [entry["phone_number"] for entry in wallet_group.user_phone_numbers if "phone_number" in entry]

    users = db.query(User).filter(User.phone_number.in_(phone_numbers)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found in this wallet group")

    user_id_map = {user.id: user for user in users}
    user_ids = list(user_id_map.keys())

    wallets = db.query(Wallet).filter(Wallet.user_id.in_(user_ids)).all()

    result = []
    for wallet in wallets:
        user = user_id_map.get(wallet.user_id)
        result.append({
            "wallet_id": wallet.id,
            "user_id": user.id,
            "user_name": user.full_name if hasattr(user, "full_name") else None,
            "phone_number": user.phone_number,
            "email": user.company_email,
            "wallet_amount": wallet.wallet_amount,
            "balance_amount": wallet.balance_amount,
            "expiry_at": wallet.expiry_at,
            "is_retainable": wallet.is_retainable,
        })

    return result



def update_wallet_group(db: Session, group_id: str, update_data: WalletGroupUpdate):
    wallet_group = db.query(WalletGroup).filter(WalletGroup.id == group_id).first()
    if not wallet_group:
        raise HTTPException(status_code=404, detail="Wallet group not found")

    if update_data.group_name is not None:
        wallet_group.group_name = update_data.group_name

    if update_data.user_phone_numbers is not None:
        wallet_group.user_phone_numbers = [{"phone_number": phone} for phone in update_data.user_phone_numbers]

    db.commit()
    db.refresh(wallet_group)
    return wallet_group





def add_user_to_wallet_group(db: Session, data: WalletGroupUserAdd):
    group = db.query(WalletGroup).filter(WalletGroup.id == data.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Wallet group not found")

    user = db.query(User).filter(User.phone_number == data.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with given phone number not found")

    # Check if user already in group
    if any(u['phone_number'] == user.phone_number for u in group.user_phone_numbers):
        raise HTTPException(status_code=400, detail="User already in the wallet group")

    group.user_phone_numbers.append({
        "id": user.id,
        "phone_number": user.phone_number,
        "email": user.company_email
    })

    # Also create a Wallet for the user in this group
    wallet = Wallet(
        user_id=user.id,
        building_id=group.building_id,
        group_id=group.id,
        wallet_amount=0,
        balance_amount=0,
        is_retainable=False
    )
    db.add(wallet)
    db.commit()
    db.refresh(group)
    return group


def remove_user_from_wallet_group(db: Session, data: WalletGroupUserRemove):
    group = db.query(WalletGroup).filter(WalletGroup.id == data.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Wallet group not found")

    user = db.query(User).filter(User.phone_number == data.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    before_count = len(group.user_phone_numbers)
    group.user_phone_numbers = [
        u for u in group.user_phone_numbers if u["phone_number"] != data.phone_number
    ]
    after_count = len(group.user_phone_numbers)

    if before_count == after_count:
        raise HTTPException(status_code=400, detail="User not in the wallet group")

    # Also delete user's wallet in that group
    db.query(Wallet).filter(
        Wallet.user_id == user.id,
        Wallet.group_id == group.id
    ).delete()

    db.commit()
    db.refresh(group)
    return group