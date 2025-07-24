from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.db.session import get_db
from schemas.user.order import OrderCreate, OrderOut, OrderDetailedOut
from service.user.order import (
    create_order,
    get_orders_by_user_id,
    get_order_by_id,                    # ✅ New: single detailed order
    get_orders_by_user_id_enriched      # ✅ New: all detailed orders
)

order_router = APIRouter(prefix="/orders", tags=["Order"])

# ✅ Place a new order
@order_router.post("/place", response_model=OrderOut)
def place_order(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order(db=db, payload=payload)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get all orders by user_id (basic)
@order_router.get("/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    try:
        orders = get_orders_by_user_id(db=db, user_id=user_id)
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user")
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get single enriched order by order_id
@order_router.get("/{order_id}", response_model=OrderDetailedOut)
def get_order_detail(order_id: str, db: Session = Depends(get_db)):
    try:
        order = get_order_by_id(db=db, order_id=order_id)
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get all enriched orders for a user
@order_router.get("/user/details/{user_id}", response_model=List[OrderDetailedOut])
def get_enriched_user_orders(user_id: str, db: Session = Depends(get_db)):
    try:
        orders = get_orders_by_user_id_enriched(db=db, user_id=user_id)
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user")
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
