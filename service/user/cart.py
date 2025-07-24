from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user.cart import Cart
from models.user.cart_items import CartItem
from models.admin.items import Item
from schemas.user.cart import CartBulkAddRequest, CartItemCreate, CartItemUpdate, CartItemRemove, CartOut


# ✅ Single item add (keep this)
def add_item_to_cart(db: Session, item_data: CartItemCreate):
    item = db.query(Item).filter(Item.id == item_data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart = db.query(Cart).filter(Cart.user_id == item_data.user_id).first()

    if cart:
        if cart.stall_id != item.stall_id:
            raise HTTPException(status_code=400, detail="You can only add items from one stall at a time")
    else:
        cart = Cart(user_id=item_data.user_id, stall_id=item.stall_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item.id
    ).first()

    if cart_item:
        cart_item.quantity += item_data.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            item_id=item.id,
            quantity=item_data.quantity,
            price_at_addition=item.final_price or item.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return cart


# ✅ Bulk item add (add this back!)
def add_items_to_cart(db: Session, payload: CartBulkAddRequest):
    user_id = payload.user_id
    items = payload.items

    if not items:
        raise HTTPException(status_code=400, detail="No items provided")

    first_item = db.query(Item).filter(Item.id == items[0].item_id).first()
    if not first_item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if cart:
        if cart.stall_id != first_item.stall_id:
            raise HTTPException(
                status_code=400,
                detail="You can only add items from one stall at a time"
            )
    else:
        cart = Cart(user_id=user_id, stall_id=first_item.stall_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    for entry in items:
        item = db.query(Item).filter(Item.id == entry.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {entry.item_id} not found")

        if item.stall_id != cart.stall_id:
            raise HTTPException(
                status_code=400,
                detail="All items must be from the same stall"
            )

        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.item_id == item.id
        ).first()

        if cart_item:
            cart_item.quantity += entry.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                item_id=item.id,
                quantity=entry.quantity,
                price_at_addition=item.final_price or item.price
            )
            db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return cart


def get_user_cart(db: Session, user_id: str):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart



def update_cart_item_quantity(db: Session, payload: CartItemUpdate):
    user_id = payload.user_id
    item_id = payload.item_id
    new_quantity = payload.quantity

    # ✅ Get cart for the user
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # ✅ Find the specific item in the cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if new_quantity <= 0:
        # Remove item if quantity is 0 or less
        db.delete(cart_item)
    else:
        # Update quantity
        cart_item.quantity = new_quantity

    db.commit()
    db.refresh(cart)
    return cart




def remove_cart_item(db: Session, payload: CartItemRemove):
    user_id = payload.user_id
    item_id = payload.item_id

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return cart



def delete_cart(db: Session, user_id: str):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Delete all associated cart items first
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    # Then delete the cart itself
    db.delete(cart)

    db.commit()
    return {"message": "Cart deleted successfully"}
