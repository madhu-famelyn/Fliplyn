import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text, func
from sqlalchemy.orm import relationship
from config.db.session import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=True)
    manager_id = Column(String, ForeignKey("managers.id"), nullable=True)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)
    stall_id = Column(String, ForeignKey("stalls.id"), nullable=False)

    created_datetime = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_datetime = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    admin = relationship("Admin", back_populates="categories")
    manager = relationship("Manager", back_populates="categories")
    building = relationship("Building", back_populates="categories")
    stall = relationship("Stall", back_populates="categories")
    items = relationship("Item", back_populates="category", cascade="all, delete-orphan")

