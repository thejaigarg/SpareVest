from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from app.schemas.base import OrmModel
class StockBase(OrmModel):
    ticker: str
    name: str
    currency: str

    class Config:
        orm_mode = True

class StockCreate(StockBase):
    # if you need any extra create-only fields, add them here
    pass

class StockUpdate(OrmModel):
    name: Optional[str] = None
    currency: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True

class StockSummary(StockBase):
    id: int

class StockQuote(OrmModel):
    last_price: Decimal | None
    day_open:  Decimal | None
    day_high:  Decimal | None
    day_low:   Decimal | None
    prev_close:Decimal | None
    fetched_at:datetime    | None

    class Config:
        orm_mode = True

class StockDetail(StockSummary):
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    quote: Optional[StockQuote] = None
