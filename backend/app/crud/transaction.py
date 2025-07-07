# DB access logic for transaction.py
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.portfolio import Portfolio
from app.models.bank_account import BankAccount
from app.models.user import User
from app.schemas.transaction import TransactionCreate
import math

def calculate_round_up(amount: float) -> float:
    if amount > 0:
        if amount < 10:
            nearest_multiple = 10
        elif amount < 100:
            nearest_multiple = math.ceil(amount / 10) * 10
        else:
            nearest_multiple = math.ceil(amount / 100) * 100
        round_up = round(nearest_multiple - amount, 2)
        return round_up
    return 0.0

def create_transaction(db: Session, user_id: int, tx: TransactionCreate):
    round_up = calculate_round_up(tx.amount)
    db_tx = Transaction(
        user_id=user_id,
        bank_account_id=tx.bank_account_id,
        amount=tx.amount,
        description=tx.description,
        round_up_amount=round_up,
        type = getattr(tx, 'type', 'purchase')
    )
    db.add(db_tx)

    if db_tx.type=="purchase":
        portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
        portfolio.roundup_bucket+=round_up

        bank_account = db.query(BankAccount).filter_by(id=tx.bank_account_id).first()
        if bank_account.balance<tx.amount:
            raise Exception("Insufficient Funds")
    
    if portfolio.roundup_bucket >= portfolio.savings_goal:
        transfer_roundup(db, user_id, tx.bank_account_id)
    
        bank_account.balance-=tx.amount
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_user_transactions(db: Session, user_id: int, limit: int = 10, offset: int = 0):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def transfer_roundup(db: Session, user_id:int, bank_account_id: int):
    portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
    user = db.query(User).get(user_id)
    bank_account = db.query(BankAccount).filter_by(id = bank_account_id, user_id=user_id).first()
    amount = portfolio.roundup_bucket

    if amount == 0 or bank_account.balance<amount:
        raise Exception("Cannot transfer: insufficient funds or zero bucket.")
    
    db_tx = Transaction(
        user_id = user_id,
        bank_account_id=bank_account_id,
        amount=amount,
        description = "Round-up sweep to savings",
        round_up_amount = 0,
        type = "deposit_to_app"
    )

    db.add(db_tx)
    bank_account.balance -= amount
    portfolio.sparevest_balance += amount
    portfolio.roundup_bucket = 0
    db.commit()
    db.refresh(db_tx)
    return db_tx