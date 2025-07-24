from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid
import enum

# ✅ Define Enum for valid countries
class CountryEnum(str, enum.Enum):
    india = "India"
    kenya = "Kenya"
    usa = "USA"
    philippines = "Philippines"
    canada = "Canada"
    malaysia = "Malaysia"
    ksa = "KSA"
    bahrain = "Bahrain"
    nepal = "Nepal"
    ireland = "Ireland"
    nigeria = "Nigeria"
    finland = "Finland"
    china = "China"
    japan = "Japan"
    denmark = "Denmark"
    france = "France"
    south_korea = "South Korea"

# ✅ Country Selection Model
class CountrySelection(Base):
    __tablename__ = "country"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    admin_id = Column(String, ForeignKey("admin_users.id"), nullable=False, unique=True)
    selected_country = Column(Enum(CountryEnum), nullable=False)

    # Optional: relationship to Admin
    admin = relationship("Admin", backref="country")


    states = relationship("State", back_populates="country")
    cities = relationship("City", back_populates="country")  # ✅ FIXED
    buildings = relationship("Building", back_populates="country")

