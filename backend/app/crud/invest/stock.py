# app/crud/invest/stock.py

from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.invest.stock import Stock
from app.schemas.invest import stock as stock_schema


def get_stock(db: Session, stock_id: int) -> Optional[stock_schema.StockDetail]:
    """
    Fetch a single stock by its ID, including its latest quote.
    """
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        return None
    return stock_schema.StockDetail.from_orm(db_stock)


def get_stock_by_ticker(db: Session, ticker: str) -> Optional[stock_schema.StockDetail]:
    """
    Fetch a single stock by its ticker symbol.
    """
    db_stock = db.query(Stock).filter(Stock.ticker == ticker).first()
    if not db_stock:
        return None
    return stock_schema.StockDetail.from_orm(db_stock)


def get_stocks(db: Session, skip: int = 0, limit: int = 100) -> List[stock_schema.StockSummary]:
    """
    List stocks (without quote details) for pagination.
    """
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    return [stock_schema.StockSummary.from_orm(s) for s in stocks]


def create_stock(db: Session, stock_in: stock_schema.StockCreate) -> stock_schema.StockDetail:
    """
    Create a new stock record.
    """
    db_stock = Stock(
        ticker=stock_in.ticker,
        name=stock_in.name,
        currency=stock_in.currency,
        is_active=stock_in.is_active,
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return stock_schema.StockDetail.from_orm(db_stock)


def update_stock(
    db: Session,
    stock_id: int,
    stock_in: stock_schema.StockUpdate
) -> Optional[stock_schema.StockDetail]:
    """
    Update mutable stock fields (name, is_active).
    """
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        return None

    if stock_in.name is not None:
        db_stock.name = stock_in.name
    if stock_in.is_active is not None:
        db_stock.is_active = stock_in.is_active

    db_stock.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_stock)
    return stock_schema.StockDetail.from_orm(db_stock)


def update_stock_quote(
    db: Session,
    stock_id: int,
    *,
    last_price: Optional[Decimal] = None,
    day_open: Optional[Decimal] = None,
    day_high: Optional[Decimal] = None,
    day_low: Optional[Decimal] = None,
    prev_close: Optional[Decimal] = None,
    fetched_at: Optional[datetime] = None,
) -> Optional[stock_schema.StockDetail]:
    """
    Update only the quote fields of a stock.
    """
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        return None

    if last_price is not None:
        db_stock.last_price = last_price
    if day_open is not None:
        db_stock.day_open = day_open
    if day_high is not None:
        db_stock.day_high = day_high
    if day_low is not None:
        db_stock.day_low = day_low
    if prev_close is not None:
        db_stock.prev_close = prev_close
    if fetched_at is not None:
        db_stock.quote_fetched_at = fetched_at

    db.commit()
    db.refresh(db_stock)
    return stock_schema.StockDetail.from_orm(db_stock)


def delete_stock(db: Session, stock_id: int) -> bool:
    """
    Soft-delete or hard-delete a stock. Adjust according to your policy.
    """
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not db_stock:
        return False

    # Example of soft-delete:
    db_stock.is_active = False
    db_stock.updated_at = datetime.utcnow()

    # Or for a hard delete, uncomment the following:
    # db.delete(db_stock)

    db.commit()
    return True
