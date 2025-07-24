import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func, text
from sqlalchemy.orm import relationship
from config.db.session import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    
    # ✅ Add this line for password storage
    password = Column(String, nullable=False)

    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=False)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)

    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    admin = relationship("Admin", back_populates="managers")
    building = relationship("Building", back_populates="managers")
    # Add this in Manager class
    categories = relationship("Category", back_populates="manager")
    stalls = relationship("Stall", back_populates="manager", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="manager", cascade="all, delete-orphan")



