from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.back_account import BankAccountCreate, BankAccountInDB
from app.crud import bank_account as crud_bank
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/bank-accounts",
    tags=["bank-accounts"],
)

@router.post("/", response_model=BankAccountInDB)
def link_bank_account(
    bank: BankAccountCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return crud_bank.create_bank_account(db, user_id=current_user.id, bank=bank)

@router.get("/", response_model=list[BankAccountInDB])
def list_bank_accounts(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return crud_bank.get_user_bank_accounts(db, user_id=current_user.id)