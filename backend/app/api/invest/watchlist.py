# app/api/watchlist.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from typing import List

from app.schemas.stocks import WatchlistEntry, WatchlistCreate
from app.crud import stocks as crud_stocks
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/", response_model=List[WatchlistEntry])
def get_watchlist(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.get_watchlist(db, user_id=current_user.id)

@router.post("/", response_model=WatchlistEntry, status_code=201)
def add_to_watchlist(
    payload: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return crud_stocks.add_watchlist(
        db,
        user_id=current_user.id,
        stock_id=payload.stockId,
    )

@router.delete("/{stock_id}", status_code=204)
def remove_from_watchlist(
    stock_id: int = Path(..., description="The ID of the stock"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    crud_stocks.remove_watchlist(
        db,
        user_id=current_user.id,
        stock_id=stock_id,
    )
