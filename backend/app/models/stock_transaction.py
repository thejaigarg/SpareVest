# app/models/stock_transaction.py

from sqlalchemy import (
    Column, Integer, ForeignKey, String, Numeric, DateTime, func
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class StockTransaction(Base):
    __tablename__ = "stock_transaction"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("user.id"), nullable=False)
    stock_id         = Column(Integer, ForeignKey("stock.id"), nullable=False)
    type             = Column(String(10), nullable=False)  # BUY or SELL
    quantity         = Column(Numeric, nullable=False)
    price_per_share  = Column(Numeric, nullable=False)
    total_amount     = Column(Numeric, nullable=False)
    timestamp        = Column(DateTime, server_default=func.now())

    user             = relationship("User", back_populates="stock_transactions")
    stock            = relationship("Stock", back_populates="transactions")
