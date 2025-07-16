# Pydantic schema for user.py
from pydantic import BaseModel, EmailStr
from app.schemas.base import OrmModel

class UserClass(OrmModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserClass):
    password: str
    currency: str

class UserInDB(UserClass):
    id: int
    is_active: bool
    role: str
    currency: str

    class Config:
        from_attributes = True

class PasswordResetRequest(OrmModel):
    email: EmailStr

class PasswordResetConfirm(OrmModel):
    token: str
    new_password: str