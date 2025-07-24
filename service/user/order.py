from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from models.user.user import User
from models.admin.items import Item
from models.admin.stalls import Stall
from models.user.wallet import Wallet
from models.user.order import Order
from schemas.user.order import OrderCreate, OrderItem
from datetime import datetime
import uuid


def create_order(db: Session, payload: OrderCreate) -> Order:
    # ✅ Validate user
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Prepare order summary
    item_summary = []
    total = 0.0

    for entry in payload.items:
        item = db.query(Item).filter(Item.id == entry.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {entry.item_id} not found")

        item_total = item.final_price * entry.quantity
        item_summary.append({
            "item_id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.final_price,
            "quantity": entry.quantity,
            "total": item_total
        })
        total += item_total

    # ✅ Deduct from wallet if needed
    if payload.pay_with_wallet:
        wallet = db.query(Wallet).filter(Wallet.user_id == payload.user_id).first()
        if not wallet:
            raise HTTPException(status_code=400, detail="Wallet not found")

        if wallet.balance_amount < total:
            raise HTTPException(status_code=400, detail="Insufficient wallet balance")

        wallet.balance_amount -= total
        db.commit()
        db.refresh(wallet)

    # ✅ Create order entry
    new_order = Order(
        id=str(uuid.uuid4()),
        user_id=user.id,
        user_phone=payload.user_phone,
        user_email=payload.user_email,
        order_details=item_summary,
        total_amount=total,
        paid_with_wallet=payload.pay_with_wallet,
        created_datetime=datetime.utcnow()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order



def get_orders_by_user_id(db: Session, user_id: str) -> List[Order]:
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_datetime.desc()).all()
    return orders





def get_order_by_id(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    enriched_items = []
    for item_entry in order.order_details:
        item = db.query(Item).filter(Item.id == item_entry["item_id"]).first()
        if not item:
            continue  # skip if item not found

        stall = db.query(Stall).filter(Stall.id == item.stall_id).first()
        stall_name = stall.name if stall else "Unknown Stall"
        stall_image_url = stall.image_url if stall else ""

        enriched_items.append({
            "item_id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.final_price,
            "quantity": item_entry["quantity"],
            "total": item_entry["total"],
            "stall_id": item.stall_id,
            "stall_name": stall_name,
            "stall_image_url": stall_image_url
        })

    return {
        "id": order.id,
        "user_id": order.user_id,
        "user_phone": order.user_phone,
        "user_email": order.user_email,
        "order_details": enriched_items,
        "total_amount": order.total_amount,
        "paid_with_wallet": order.paid_with_wallet,
        "created_datetime": order.created_datetime
    }


def get_orders_by_user_id_enriched(db: Session, user_id: str):
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_datetime.desc()).all()
    if not orders:
        return []

    response = []

    for order in orders:
        enriched_items = []

        for item_entry in order.order_details:
            item = db.query(Item).filter(Item.id == item_entry["item_id"]).first()
            if not item:
                continue

            stall = db.query(Stall).filter(Stall.id == item.stall_id).first()
            stall_name = stall.name if stall else "Unknown Stall"
            stall_image_url = stall.image_url if stall else ""

            enriched_items.append({
                "item_id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.final_price,
                "quantity": item_entry["quantity"],
                "total": item_entry["total"],
                "stall_id": item.stall_id,
                "stall_name": stall_name,
                "stall_image_url": stall_image_url
            })

        response.append({
            "id": order.id,
            "user_id": order.user_id,
            "user_phone": order.user_phone,
            "user_email": order.user_email,
            "order_details": enriched_items,
            "total_amount": order.total_amount,
            "paid_with_wallet": order.paid_with_wallet,
            "created_datetime": order.created_datetime
        })

    return response