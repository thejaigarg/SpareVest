# backend/app/main.py
# backend/app/main.py

from fastapi import FastAPI
from app.api import user as user_router

app = FastAPI()

app.include_router(user_router.router)