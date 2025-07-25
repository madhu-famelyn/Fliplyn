import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db.session import Base
from models.admin.admin import Admin
from models.admin.country import CountrySelection
from models.admin.state import State

class City(Base):
    __tablename__ = "cities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=False)
    country_id = Column(String, ForeignKey("country.id"), nullable=False)
    state_id = Column(String, ForeignKey("states.id"), nullable=False)
    city = Column(String, nullable=False)
    city_id = Column(String, nullable=False)  # ✅ New column for short-form city ID

    admin = relationship("Admin", back_populates="cities")
    country = relationship("CountrySelection", back_populates="cities")
    state = relationship("State", back_populates="cities")
    buildings = relationship("Building", back_populates="city")
