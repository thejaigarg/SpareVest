# Ensure all models are imported so Base.metadata is aware of them:

from .savings.transaction import Transaction

from .user import User
from .savings.bank_account import BankAccount
from .savings.portfolio import Portfolio

__all__ = [
    "Transaction",
    "User",
    "BankAccount",
    "Portfolio"
]

# Base is imported by alembic/env.py separately