# backend/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from app.api import user as user_router
from app.api import auth as auth_router
from app.api import bank_account as bank_account_router
from app.api import transactions as transctions
from app.core.config import FRONTEND_URL

app = FastAPI()

# Health-check endpoint
@app.get("/healthz")
async def healthz():
    return JSONResponse({"status": "ok"})

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the SpareVest API"}

# CORS configuration
origins = [
    "http://localhost:80",
    "http://localhost",
    FRONTEND_URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your API routers
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(bank_account_router.router)
app.include_router(transctions.router)
