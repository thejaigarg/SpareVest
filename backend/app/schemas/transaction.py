# Pydantic schema for transaction.py
from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    bank_account_id: int

class TransactionInDB(TransactionBase):
    id: int
    user_id: int
    bank_account_id: int
    date: datetime
    round_up_amount: float

    class Config:
        from_attributes = True