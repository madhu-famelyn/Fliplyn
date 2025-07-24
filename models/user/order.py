# models/user/order.py

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user_email = Column(String, nullable=False)
    user_phone = Column(String, nullable=False)

    order_details = Column(JSON, nullable=False)  # list of items with price, qty, name, desc
    total_amount = Column(Float, nullable=False)

    paid_with_wallet = Column(Boolean, default=False)

    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="orders")
