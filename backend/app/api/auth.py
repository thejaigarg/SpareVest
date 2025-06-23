# API routes for auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
import os

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.responses import JSONResponse

from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token, hash_password
from app.crud.user import authenticate_user, get_user_by_email, update_user_password
from app.core.email import send_reset_email
from app.schemas.user import UserInDB, PasswordResetRequest, PasswordResetConfirm

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/logout")
def logout():
    """
    Instruct the client to delete JWT from memory/local storage.
    Stateless JWT cannot be revoked server-side without
    extra infrastructure (like a blacklist).
    """
    return JSONResponse(
        content={"msg": "Successfully logged out. Please remove your access token on the client."}
    )