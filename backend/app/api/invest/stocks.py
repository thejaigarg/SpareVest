# app/api/routers/stock.py

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.invest import stock as stock_crud
from app.schemas.invest import stock as stock_schema
from app.models.invest.stock import Stock
from app.core.database import get_db

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)


@router.get("/all", response_model=List[stock_schema.StockSummary])
def list_stocks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return stock_crud.get_stocks(db, skip=skip, limit=limit)


@router.get("/{stock_id}", response_model=stock_schema.StockDetail)
def read_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    stock = stock_crud.get_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock


@router.get("/by-ticker/{ticker}", response_model=stock_schema.StockDetail)
def read_stock_by_ticker(
    ticker: str,
    db: Session = Depends(get_db)
):
    stock = stock_crud.get_stock_by_ticker(db, ticker=ticker.upper())
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock


@router.post("/create", response_model=stock_schema.StockDetail, status_code=status.HTTP_201_CREATED)
def create_stock(
    stock_in: stock_schema.StockCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Stock).filter(Stock.ticker == stock_in.ticker).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker already exists"
        )
    return stock_crud.create_stock(db, stock_in)


@router.put("/{stock_id}", response_model=stock_schema.StockDetail)
def update_stock(
    stock_id: int,
    stock_in: stock_schema.StockUpdate,
    db: Session = Depends(get_db)
):
    updated = stock_crud.update_stock(db, stock_id, stock_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return updated


@router.patch("/{stock_id}/quote", response_model=stock_schema.StockDetail)
def patch_stock_quote(
    stock_id: int,
    quote: stock_schema.StockQuote,
    db: Session = Depends(get_db)
):
    updated = stock_crud.update_stock_quote(
        db,
        stock_id,
        last_price=quote.last_price,
        day_open=quote.day_open,
        day_high=quote.day_high,
        day_low=quote.day_low,
        prev_close=quote.prev_close,
        fetched_at=quote.fetched_at or datetime.utcnow()
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return updated


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    success = stock_crud.delete_stock(db, stock_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return
