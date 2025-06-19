# API routes for deps.py
# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core.security import decode_access_token  # import your util!
from app.core.database import get_db
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user