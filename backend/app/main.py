# backend/app/main.py
# backend/app/main.py

from fastapi import FastAPI
from app.api import user as user_router
from app.api import auth as auth_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(auth_router.router)