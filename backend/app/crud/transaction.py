# DB access logic for transaction.py
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

def calculate_round_up(amount: float) -> float:
    # Only for positive "purchase" transactions
    if amount > 0:
        cents = amount % 1
        round_up = (1 - cents) if cents != 0 else 0
        return round(round_up, 2)
    return 0.0

def create_transaction(db: Session, user_id: int, tx: TransactionCreate):
    round_up = calculate_round_up(tx.amount)
    db_tx = Transaction(
        user_id=user_id,
        bank_account_id=tx.bank_account_id,
        amount=tx.amount,
        description=tx.description,
        round_up_amount=round_up
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_user_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()