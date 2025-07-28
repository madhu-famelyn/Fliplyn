from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid

class WalletGroup(Base):
    __tablename__ = "wallet_groups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    group_name = Column(String, nullable=False)
    user_phone_numbers = Column(JSON, nullable=False)

    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    building = relationship("Building", back_populates="wallet_groups")
