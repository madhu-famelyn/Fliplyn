from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from config.db.session import Base
from datetime import datetime
import pytz
import uuid

# Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user_email = Column(String, nullable=False)
    user_phone = Column(String, nullable=False)

    order_details = Column(JSON, nullable=False)  # List of items with price, qty, name, desc
    total_amount = Column(Float, nullable=False)

    paid_with_wallet = Column(Boolean, default=False)

    token_number = Column(Integer, nullable=False, index=True)

    created_datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(IST)
    )

    updated_datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(IST),
        onupdate=lambda: datetime.now(IST)
    )

    user = relationship("User", backref="orders")
