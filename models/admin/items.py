import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func

from config.db.session import Base



class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    tax_included = Column(Boolean, default=False)
    Gst_precentage = Column(Float, nullable=True)
    final_price = Column(Float, nullable=True)  # GST percentage, e.g., 0.10 for 10%

    is_available = Column(Boolean, default=True)  # ✅ New field added here

    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=True)
    manager_id = Column(String, ForeignKey("managers.id"), nullable=True)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)
    stall_id = Column(String, ForeignKey("stalls.id"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)

    admin = relationship("Admin", back_populates="items", foreign_keys=[admin_id])
    manager = relationship("Manager", back_populates="items", foreign_keys=[manager_id])
    building = relationship("Building", back_populates="items")
    stall = relationship("Stall", back_populates="items")
    category = relationship("Category", back_populates="items")

    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), onupdate=func.now())
