# app/api/invest/stocks.py
from fastapi import APIRouter, Depends, Query, Path
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.stocks import StockSummary, StockDetail, PricePoint
from app.crud import stocks as crud_stocks
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/stocks", tags=["stocks"])

@router.get("/all", response_model=List[StockSummary])
def get_all_stocks(
    q: Optional[str] = Query(None, description="Search term for ticker or name"),
    active: bool = Query(True, description="Filter active stocks"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.list_stocks(db, q=q, active=active, page=page, limit=limit)

@router.get("/{stock_id}", response_model=StockDetail)
def get_stock_detail(
    stock_id: int = Path(..., description="The ID of the stock"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.get_stock(db, stock_id)

@router.get("/{stock_id}/history", response_model=List[PricePoint])
def get_stock_history(
    stock_id: int = Path(..., description="The ID of the stock"),
    from_date: Optional[str] = Query(None, alias="from", description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, alias="to", description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.get_price_history(db, stock_id, from_date, to_date)
