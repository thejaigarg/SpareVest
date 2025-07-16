from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Holding(Base):
    __tablename__ = "holding"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    quantity = Column(Numeric, nullable=False, default=0)
    avg_cost = Column(Numeric, nullable=False, default=0)
    last_price = Column(Numeric, nullable=True)
    market_value = Column(Numeric, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="holdings")
    stock = relationship("Stock", back_populates="holdings")
