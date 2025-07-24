# models/user.py

from sqlalchemy import Column, String, TIMESTAMP, func, text, Boolean
from config.db.session import Base
from sqlalchemy.orm import relationship 
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    company_email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)

    otp = Column(String, nullable=True)  # stores latest OTP sent
    is_otp_verified = Column(Boolean, nullable=False, default=False)
    otp_verified_via = Column(String, nullable=True)  # either 'email' or 'phone'

    created_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )



    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete")
    wallet = relationship("Wallet", back_populates="user", uselist=False)

