import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db.session import Base


class State(Base):
    __tablename__ = "states"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    state_id = Column(String, unique=False, nullable=False)  # ✅ e.g., "00001", "00002"
    state_name = Column(String, nullable=False)             # ✅ e.g., "Andhra Pradesh"

    vendor_id = Column(String, ForeignKey("admin_users.id"), nullable=False)
    country_id = Column(String, ForeignKey("country.id"), nullable=False)

    # Relationships
    vendor = relationship("Admin", back_populates="states")
    country = relationship("CountrySelection", back_populates="states")
    cities = relationship("City", back_populates="state")
    buildings = relationship("Building", back_populates="state")
