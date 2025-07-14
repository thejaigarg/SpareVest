# app/api/transactions.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from typing import List, Optional

from app.schemas.stocks import TransactionRecord, TransactionCreate
from app.crud import stocks as crud_stocks
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/stock-transactions", tags=["transactions"])

@router.get("/", response_model=List[TransactionRecord])
def list_stock_transactions (
    type: Optional[str] = Query(None, regex="^(BUY|SELL)$"),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.list_stock_transactions(
        db,
        user_id=current_user.id,
        type=type,
        from_date=from_date,
        to_date=to_date,
        page=page,
        limit=limit,
    )

@router.post("/", response_model=TransactionRecord, status_code=201)
def create_stock_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.create_stock_transaction(
        db,
        user_id=current_user.id,
        tx=payload,
    )
