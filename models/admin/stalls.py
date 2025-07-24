import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func, text
from sqlalchemy.orm import relationship
from config.db.session import Base

class Stall(Base):
    __tablename__ = "stalls"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    image_url = Column(String, nullable=True)  # ✅ Add this line for image support

    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)
    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=True)
    manager_id = Column(String, ForeignKey("managers.id"), nullable=True)

    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    categories = relationship("Category", back_populates="stall")
    building = relationship("Building", back_populates="stalls")
    admin = relationship("Admin", back_populates="stalls")
    manager = relationship("Manager", back_populates="stalls")
    items = relationship("Item", back_populates="stall", cascade="all, delete-orphan")

