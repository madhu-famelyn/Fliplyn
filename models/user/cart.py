# models/cart.py

import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from config.db.session import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stall_id = Column(String, ForeignKey("stalls.id"), nullable=False)  # Enforces single-stall cart

    user = relationship("User", back_populates="cart")
    stall = relationship("Stall")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete")

    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), onupdate=func.now())
