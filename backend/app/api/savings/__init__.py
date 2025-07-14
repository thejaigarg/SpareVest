
# backend/app/api/savings/__init__.py

from .bank_account import router as bank_account_router
from .portfolio import router as portfolio_router
from .transactions import router as transactions_router

# Aggregate all Savings feature routers
savings_routers = [
    bank_account_router,
    portfolio_router,
    transactions_router,
]
