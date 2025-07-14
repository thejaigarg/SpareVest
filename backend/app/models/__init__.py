# Ensure all models are imported so Base.metadata is aware of them:
from .stock import Stock
from .holding import Holding
from .stock_transaction import StockTransaction
from .transaction import Transaction
from .watchlist_entry import WatchlistEntry
from .price_history import PriceHistory
from .user import User
from .bank_account import BankAccount
from .portfolio import Portfolio

__all__ = [
    "Stock",
    "Holding",
    "StockTransaction",
    "Transaction",
    "WatchlistEntry",
    "PriceHistory",
    "User",
    "BankAccount",
    "Portfolio",
]

# Base is imported by alembic/env.py separately