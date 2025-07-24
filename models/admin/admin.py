from sqlalchemy import Column, String, func, TIMESTAMP, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from config.db.session import Base
import uuid
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = "admin_users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String, nullable=True)
    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP") )
    updated_datetime = Column( TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


    states = relationship("State", back_populates="vendor")
    cities = relationship("City", back_populates="admin")
    buildings = relationship("Building", back_populates="user")
    managers = relationship("Manager", back_populates="admin")
    categories = relationship("Category", back_populates="admin")
    stalls = relationship("Stall", back_populates="admin", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="admin", cascade="all, delete-orphan")




