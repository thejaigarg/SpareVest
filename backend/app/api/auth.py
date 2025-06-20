# API routes for auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
import os

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

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

@router.post("/auth/password-reset/request")
async def password_reset_request(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, data.email)
    msg = "If an account with that email exists, you'll receive a password reset link."

    if not user:
        return {"msg": msg}

    reset_token = create_access_token(
        data={"sub": user.email, "scope": "password_reset"},
        expires_delta=timedelta(minutes=30),
    )
    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    background_tasks.add_task(send_reset_email, user.email, reset_link)
    return {"msg": msg}

@router.post("/auth/password-reset/confirm")
async def password_reset_confirm(
    data: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(data.token)
        email = payload.get("sub")
        scope = payload.get("scope")
        if (email is None) or (scope != "password_reset"):
            raise HTTPException(status_code=400, detail="Invalid token.")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Set hashed password
    new_hashed = hash_password(data.new_password)
    update_user_password(db=db, user=user, new_hashed_password=new_hashed)

    return {"msg": "Password updated successfully."}