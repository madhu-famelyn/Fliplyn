from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=True)

    wallet_amount = Column(Float, nullable=False, default=0.0)
    balance_amount = Column(Float, nullable=False, default=0.0)
    expiry_at = Column(DateTime(timezone=True), nullable=True)
    is_retainable = Column(Boolean, default=False)

    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="wallets")
    building = relationship("Building", back_populates="wallets")
