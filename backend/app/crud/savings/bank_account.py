from sqlalchemy.orm import Session
from app.models.savings.bank_account import BankAccount
from app.schemas.savings.back_account import BankAccountCreate

def create_bank_account(db: Session, user_id: int, bank: BankAccountCreate):

    existing_accounts = db.query(BankAccount).filter_by(user_id=user_id).count()
    is_default = existing_accounts == 0

    db_bank = BankAccount(
        user_id=user_id,
        bank_name=bank.bank_name,
        account_number=bank.account_number,
        currency=bank.currency,
        balance=1000000000.0,
        is_default = is_default
    )
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

def get_user_bank_accounts(db: Session, user_id: int):
    return db.query(BankAccount).filter(BankAccount.user_id == user_id).all()

def set_default_bank_account(db:Session, user_id:int, bank_account_id:int):
    db.query(BankAccount).filter_by(user_id=user_id).update({'is_default':False})
    db.query(BankAccount).filter_by(id=bank_account_id, user_id=user_id).update({'is_default':True})
    db.commit()