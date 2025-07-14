from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    date = Column(Date, nullable=False)
    close_price = Column(Numeric, nullable=False)

    # Relationships
    stock = relationship("Stock", back_populates="price_history")
