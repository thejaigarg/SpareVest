# SQLAlchemy model for user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    role = Column(String, default="user", nullable=False)   # "user" or "admin"