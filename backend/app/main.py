# backend/app/main.py
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user as user_router
from app.api import auth as auth_router

app = FastAPI()
origins = [
    "http://localhost:5173",  # Vite dev server
    # Add others as needed, e.g. "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router.router)
app.include_router(auth_router.router)