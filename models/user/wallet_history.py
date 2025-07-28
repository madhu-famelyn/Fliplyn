from sqlalchemy import Column, String, Float, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from config.db.session import Base# Assuming you're using Base for declarative_base

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    wallet_id = Column(String, ForeignKey("wallets.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)  # Optional, only for debits
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # "credit" or "debit"
    description = Column(String, nullable=True)  # e.g., "Added by Admin", "Order Payment"
    item_details = Column(JSON, nullable=True)  # Optional: For order-related transactions
    created_at = Column(DateTime, default=datetime.utcnow)

    wallet = relationship("Wallet", backref="transactions")
    user = relationship("User")
    order = relationship("Order", backref="wallet_transaction", uselist=False)
