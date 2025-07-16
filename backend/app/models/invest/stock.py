from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Numeric
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

     # — New “last quote” snapshot fields —
    last_price        = Column(Numeric, nullable=True)    # Finnhub’s `c`
    day_open          = Column(Numeric, nullable=True)    # Finnhub’s `o`
    day_high          = Column(Numeric, nullable=True)    # Finnhub’s `h`
    day_low           = Column(Numeric, nullable=True)    # Finnhub’s `l`
    prev_close        = Column(Numeric, nullable=True)    # Finnhub’s `pc`
    quote_fetched_at  = Column(DateTime, nullable=True)   # when these were last updated

    # Relationships
    holdings = relationship("Holding", back_populates="stock")
    transactions = relationship("StockTransaction", back_populates="stock")
    watchlist_entries = relationship("WatchlistEntry", back_populates="stock")
    price_history = relationship("PriceHistory", back_populates="stock")
