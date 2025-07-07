# backend/app/crud/user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from app.models.portfolio import Portfolio

from app.core.security import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        full_name=user.full_name,
        is_active=1,
        currency=user.currency
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_portfolio = Portfolio(
        user_id = db_user.id,
        savings_goal = 100.0,
        sparevest_balance = 0.0,
        roundup_bucket = 0.0
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_password(db: Session, user: User, new_hashed_password: str):
    user.hashed_password = new_hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)