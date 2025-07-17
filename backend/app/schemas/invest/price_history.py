# app/schemas/invest/price_history.py

from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.base import OrmModel

class PricePointBase(OrmModel):
    stock_id:    int
    date:        date
    open_price:  Decimal | None
    high_price:  Decimal | None
    low_price:   Decimal | None
    close_price: Decimal
    volume:      Decimal | None

class PricePointCreate(PricePointBase):
    pass

class PricePointInDB(PricePointBase):
    id: int

    class Config:
        orm_mode = True
