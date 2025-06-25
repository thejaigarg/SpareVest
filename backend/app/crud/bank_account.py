from sqlalchemy.orm import Session
from app.models.bank_account import BankAccount
from app.schemas.back_account import BankAccountCreate

def create_bank_account(db: Session, user_id: int, bank: BankAccountCreate):
    db_bank = BankAccount(
        user_id=user_id,
        bank_name=bank.bank_name,
        account_number=bank.account_number
    )
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def get_user_bank_accounts(db: Session, user_id: int):
    return db.query(BankAccount).filter(BankAccount.user_id == user_id).all()