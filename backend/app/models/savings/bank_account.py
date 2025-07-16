from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
import datetime
from app.core.database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False, unique=True)  # Store safely for demo (mask in frontend)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    currency = Column(String(3), nullable=False)
    balance = Column(Float, default = 10000000000.0)
    is_default = Column(Boolean, default = False)

    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account")