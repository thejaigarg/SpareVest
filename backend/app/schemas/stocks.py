from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Stock Reference ────────────────────────────────────────────────────────────

class StockSummary(BaseModel):
    id: int
    ticker: str
    name: str
    currency: str

class StockDetail(StockSummary):
    is_active: bool


# ── Price History ─────────────────────────────────────────────────────────────

class PricePoint(BaseModel):
    date: date
    close_price: float


# ── Holdings ─────────────────────────────────────────────────────────────────

class Holding(BaseModel):
    stockId: int
    ticker: str
    quantity: float
    avgCost: float
    lastPrice: float
    marketValue: float
    unrealizedPL: float

class HoldingsResponse(BaseModel):
    totalValue: float
    todaysChange: float
    positions: List[Holding]


# ── Transactions ──────────────────────────────────────────────────────────────
class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    
class TransactionRecord(BaseModel):
    id: int
    timestamp: datetime
    type: TransactionType
    stockId: int
    ticker: str
    quantity: float
    pricePerShare: float
    totalAmount: float

class TransactionsResponse(BaseModel):
    data: List[TransactionRecord]
    page: int
    limit: int
    total: int

class TransactionCreate(BaseModel):
    type: TransactionType
    stockId: int
    quantity: float
    pricePerShare: Optional[float]  # server can default to lastPrice if omitted


# ── Watchlist ────────────────────────────────────────────────────────────────

class WatchlistEntry(BaseModel):
    stockId: int
    ticker: str
    lastPrice: float
    dailyChangePct: float

class WatchlistCreate(BaseModel):
    stockId: int
