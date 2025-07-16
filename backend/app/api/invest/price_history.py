from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.invest import price_history 
from app.schemas.invest.price_history import PricePointInDB
from app.models.invest.stock import Stock
from app.core.database import get_db
from app.core.finnhub_client import get_finnhub_client, Client

router = APIRouter(
    prefix="/stocks",
    tags=["price_history"],
)


@router.get("/{stock_id}/history", response_model=List[PricePointInDB])
def stock_history(
    stock_id: int,
    db: Session = Depends(get_db),
    finnhub_client = Depends(get_finnhub_client)
):
    if not db.query(Stock).get(stock_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return price_history.get_or_refresh_price_history(db, stock_id, days_to_fetch=30)
