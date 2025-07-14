from .stocks import router as stocks_router
from .holdings import router as holdings_router
from .stock_transactions import router as transactions_router
from .watchlist import router as watchlist_router

# Group all Invest-feature routers under a single list
invest_routers = [
    stocks_router,
    holdings_router,
    transactions_router,
    watchlist_router,
]
