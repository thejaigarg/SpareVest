from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    holdings = relationship("Holding", back_populates="stock")
    transactions = relationship("stock_transaction", back_populates="stock")
    watchlist_entries = relationship("WatchlistEntry", back_populates="stock")
    price_history = relationship("PriceHistory", back_populates="stock")
