# Pydantic schema for user.py
from pydantic import BaseModel, EmailStr

class UserClass(BaseModel):
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
    savings_goal: float
    sparevest_balance: float

    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str