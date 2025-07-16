# SQLAlchemy model for portfolio.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Portfolio(Base):
    __tablename__="portfolios"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    #Portfolio specific stats
    name = Column(String, default="Main Portfolio")
    savings_goal=Column(Float, default=100.0, nullable=False)
    sparevest_balance = Column(Float, default=0.0, nullable=False)
    roundup_bucket = Column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="portfolio")