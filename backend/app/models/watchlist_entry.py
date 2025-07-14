from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class WatchlistEntry(Base):
    __tablename__ = "watchlist_entry"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    added_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="watchlist_entries")
    stock = relationship("Stock", back_populates="watchlist_entries")
