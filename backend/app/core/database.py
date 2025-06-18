# backend/app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# 1. Create SQLAlchemy engine (connects to your PostgreSQL DB)
engine = create_engine(
    DATABASE_URL,
    echo=True,            # set to False in production
    future=True,          # modern SQLAlchemy style
)

# 2. Create a configured "Session" class for our DB
SessionLocal = sessionmaker(
    autocommit=False,     # results are committed manually (good practice)
    autoflush=False,      # prevents unexpected DB writes
    bind=engine
)

# 3. Declare a Base class for model definitions (inherit this in your models)
Base = declarative_base()

# 4. Dependency to get DB session for FastAPI routes
def get_db():
    db = SessionLocal()   # create new session for a request
    try:
        yield db          # provide the session to the path operation
    finally:
        db.close()        # close the session after the request is handled