# app/models/invest/price_history.py

from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id          = Column(Integer, primary_key=True, index=True)
    stock_id    = Column(Integer, ForeignKey("stock.id"), nullable=False)
    date        = Column(Date, nullable=False)
    open_price  = Column(Numeric, nullable=True)
    high_price  = Column(Numeric, nullable=True)
    low_price   = Column(Numeric, nullable=True)
    close_price = Column(Numeric, nullable=False)
    volume      = Column(Numeric, nullable=True)

    stock = relationship("Stock", back_populates="price_history")
