# models/cart_item.py

import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    cart_id = Column(String, ForeignKey("carts.id"), nullable=False)
    item_id = Column(String, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    item = relationship("Item")

    # Optionally denormalized fields for fast lookup (e.g., for final price):
    price_at_addition = Column(Float, nullable=True)
