import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config.db.session import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    user_id = Column(String, ForeignKey("admin_users.id"), nullable=False)
    country_id = Column(String, ForeignKey("country.id"), nullable=False)
    state_id = Column(String, ForeignKey("states.id"), nullable=False)
    city_id = Column(String, ForeignKey("cities.id"), nullable=False)

    building_name = Column(String, nullable=False)
    city_identifier = Column(String, nullable=False) 
    user_access = Column(JSON, nullable=True)

    user = relationship("Admin", back_populates="buildings")
    country = relationship("CountrySelection")
    state = relationship("State")
    city = relationship("City")

    managers = relationship("Manager", back_populates="building")
    categories = relationship("Category", back_populates="building")
    stalls = relationship("Stall", back_populates="building", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="building", cascade="all, delete-orphan")


    wallets = relationship("Wallet", back_populates="building")

