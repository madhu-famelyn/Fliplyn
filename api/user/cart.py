from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from config.db.session import get_db
from schemas.user.cart import CartItemCreate, CartOut, CartBulkAddRequest,  CartItemUpdate, CartItemRemove
from service.user.cart import add_item_to_cart, add_items_to_cart, get_user_cart, update_cart_item_quantity, remove_cart_item, delete_cart

cart_router = APIRouter(prefix="/cart", tags=["Cart"])



@cart_router.post("/add", response_model=CartOut)
def add_to_cart(payload: CartItemCreate, db: Session = Depends(get_db)):
    """
    Add a single item to the cart.
    Only items from the same stall can be added to one cart.
    """
    return add_item_to_cart(db, item_data=payload)


@cart_router.post("/add-multiple", response_model=CartOut)
def add_multiple_items_to_cart(payload: CartBulkAddRequest, db: Session = Depends(get_db)):
    """
    Add multiple items to the cart in one request.
    All items must be from the same stall.
    """
    return add_items_to_cart(db, payload=payload)


@cart_router.get("/{user_id}", response_model=CartOut)
def get_cart(user_id: str, db: Session = Depends(get_db)):
    """
    Get the cart for a specific user by user_id.
    """
    return get_user_cart(db, user_id=user_id)



@cart_router.delete("/remove", response_model=CartOut)
def delete_cart_item(payload: CartItemRemove, db: Session = Depends(get_db)):
    """
    Remove an item from the cart.
    """
    return remove_cart_item(db, payload=payload)


@cart_router.put("/update-quantity", response_model=CartOut)
def update_item_quantity(payload: CartItemUpdate, db: Session = Depends(get_db)):
    """
    Update the quantity of an item in the cart.
    If quantity is 0 or less, the item will be removed.
    """
    return update_cart_item_quantity(db, payload=payload)



@cart_router.delete("/clear/{user_id}")
def clear_cart(user_id: str, db: Session = Depends(get_db)):
    """
    Delete the entire cart and its items for a user.
    """
    return delete_cart(db, user_id=user_id)