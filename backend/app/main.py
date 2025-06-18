# backend/app/main.py
from app.core.database import Base, engine
from app.models.user import User     # import all your models

# This creates tables if they don't exist already
# Base.metadata.create_all(bind=engine)

# This will attempt to create the 'users' table in the database
print("Creating all tables in the database (if they don't exist)...")
Base.metadata.create_all(bind=engine)
print("Successfully created tables!")
