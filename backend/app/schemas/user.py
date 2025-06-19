# Pydantic schema for user.py
from pydantic import BaseModel, EmailStr

class UserClass(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserClass):
    password: str

class UserInDB(UserClass):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    email: EmailStr