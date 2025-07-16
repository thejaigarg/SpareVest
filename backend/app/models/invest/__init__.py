# Ensure all models are imported so Base.metadata is aware of them:
from .stock import Stock
from .holding import Holding
from .stock_transaction import StockTransaction
from .watchlist_entry import WatchlistEntry
from .price_history import PriceHistory

__all__ = [
    "Stock",
    "Holding",
    "StockTransaction",
    "WatchlistEntry",
    "PriceHistory"
]

# Base is imported by alembic/env.py separately