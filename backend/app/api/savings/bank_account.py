from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.savings.back_account import BankAccountCreate, BankAccountInDB
from app.crud.savings import bank_account as crud_bank
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.savings.bank_account import BankAccount

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
    if bank.currency != current_user.currency:
        raise HTTPException(
            status_code = 400,
            detail=f"Bank account currency must amtch your profile currency ({current_user.currency})."
        )
    return crud_bank.create_bank_account(db, user_id=current_user.id, bank=bank)

@router.get("/", response_model=list[BankAccountInDB])
def list_bank_accounts(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return crud_bank.get_user_bank_accounts(db, user_id=current_user.id)

@router.post("/{bank_account_id}/make-default", response_model=BankAccountInDB)
def make_default_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bank_account = db.query(BankAccount).filter_by(id=bank_account_id, user_id=current_user.id).first()
    if not bank_account:
        raise HTTPException(404, "Bank account not found")
    crud_bank.set_default_bank_account(db, user_id=current_user.id, bank_account_id=bank_account_id)
    db.refresh(bank_account)
    return bank_account