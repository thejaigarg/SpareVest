# backend/app/main.py

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import user as user_router
from app.api import auth as auth_router
from app.api.invest import invest_routers
from app.api.savings import savings_routers

app = FastAPI()

# CORS: allow your frontend origin (or use ["*"] during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health-check
@app.get("/healthz")
async def healthz():
    return JSONResponse({"status": "ok"})

# Root
@app.get("/")
async def root():
    return {"message": "Welcome to the SpareVest API"}

# Include shared routers
app.include_router(user_router.router)
app.include_router(auth_router.router)

# Include feature-group routers
for router in invest_routers:
    app.include_router(router)

for router in savings_routers:
    app.include_router(router)
