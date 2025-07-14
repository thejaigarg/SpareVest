# backend/app/schemas/market.py
from pydantic import BaseModel

class Quote(BaseModel):
    symbol: str
    current: float
    high: float
    low: float
    open: float
    prev_close: float

