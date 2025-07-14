from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date

from app.models.stock import Stock
from app.models.holding import Holding
from app.models.stock_transaction import StockTransaction as Transaction
from app.models.watchlist_entry import WatchlistEntry
from app.models.price_history import PriceHistory
from app.schemas.stocks import StockSummary, StockDetail, PricePoint, Holding as HoldingSchema, TransactionRecord, TransactionCreate, WatchlistEntry as WatchlistSchema

# --- Stocks CRUD --------------------------------------------------------------

def list_stocks(
    db: Session, 
    q: Optional[str], 
    active: bool, 
    page: int, 
    limit: int
) -> Tuple[List[StockSummary], int]:
    query = db.query(Stock).filter(Stock.is_active == active)
    if q:
        query = query.filter(
            func.lower(Stock.ticker).contains(q.lower()) |
            func.lower(Stock.name).contains(q.lower())
        )
    total = query.count()
    stocks = query.offset((page - 1) * limit).limit(limit).all()
    data = [StockSummary.from_orm(s) for s in stocks]
    return data, total

def get_stock(db: Session, stock_id: int) -> StockDetail:
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    return StockDetail.from_orm(stock)

def get_price_history(
    db: Session, 
    stock_id: int, 
    from_date: Optional[str], 
    to_date: Optional[str]
) -> List[PricePoint]:
    query = db.query(PriceHistory).filter(PriceHistory.stock_id == stock_id)
    if from_date:
        query = query.filter(PriceHistory.date >= date.fromisoformat(from_date))
    if to_date:
        query = query.filter(PriceHistory.date <= date.fromisoformat(to_date))
    query = query.order_by(PriceHistory.date.desc())
    return [PricePoint(date=ph.date, close_price=ph.close_price) for ph in query.all()]

# --- Holdings CRUD ------------------------------------------------------------

def get_user_holdings(db: Session, user_id: int) -> HoldingSchema:
    holdings = (
        db.query(Holding, Stock)
        .join(Stock, Holding.stock_id == Stock.id)
        .filter(Holding.user_id == user_id)
        .all()
    )
    total_value = sum(h.quantity * h.last_price for h, _ in holdings)
    # Assuming todaysChange is stored or computed elsewhere; placeholder 0.0
    positions = []
    for holding, stock in holdings:
        positions.append(HoldingSchema(
            stockId=stock.id,
            ticker=stock.ticker,
            quantity=float(holding.quantity),
            avgCost=float(holding.avg_cost),
            lastPrice=float(holding.last_price),
            marketValue=float(holding.quantity * holding.last_price),
            unrealizedPL=float((holding.last_price - holding.avg_cost) * holding.quantity)
        ))
    return {"totalValue": total_value, "todaysChange": 0.0, "positions": positions}

# --- Transactions CRUD --------------------------------------------------------

def list_transactions(
    db: Session,
    user_id: int,
    type: Optional[str],
    from_date: Optional[str],
    to_date: Optional[str],
    page: int,
    limit: int
) -> Tuple[List[TransactionRecord], int]:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if type:
        query = query.filter(Transaction.type == type)
    if from_date:
        query = query.filter(Transaction.timestamp >= date.fromisoformat(from_date))
    if to_date:
        query = query.filter(Transaction.timestamp <= date.fromisoformat(to_date))
    total = query.count()
    txs = query.order_by(Transaction.timestamp.desc()).offset((page - 1) * limit).limit(limit).all()
    data = [TransactionRecord(
        id=tx.id,
        timestamp=tx.timestamp,
        type=tx.type,
        stockId=tx.stock_id,
        ticker=tx.stock.ticker,
        quantity=float(tx.quantity),
        pricePerShare=float(tx.price_per_share),
        totalAmount=float(tx.total_amount)
    ) for tx in txs]
    return data, total

def create_transaction(
    db: Session,
    user_id: int,
    tx: TransactionCreate
) -> TransactionRecord:
    # Determine price
    price = tx.pricePerShare
    if price is None:
        latest = db.query(PriceHistory).filter(PriceHistory.stock_id == tx.stockId).order_by(PriceHistory.date.desc()).first()
        price = latest.close_price
    total_amount = price * tx.quantity

    # Record transaction
    db_tx = Transaction(
        user_id=user_id,
        stock_id=tx.stockId,
        type=tx.type,
        quantity=tx.quantity,
        price_per_share=price,
        total_amount=total_amount
    )
    db.add(db_tx)

    # Upsert holding
    holding = db.query(Holding).filter_by(user_id=user_id, stock_id=tx.stockId).first()
    if not holding:
        holding = Holding(user_id=user_id, stock_id=tx.stockId, quantity=0, avg_cost=0)
        db.add(holding)
        db.flush()  # assign id
    
    # Update holding
    if tx.type == "BUY":
        new_qty = holding.quantity + tx.quantity
        new_cost = (holding.avg_cost * holding.quantity + total_amount) / new_qty
        holding.quantity = new_qty
        holding.avg_cost = new_cost
    else:  # SELL
        holding.quantity -= tx.quantity
    # Update last_price and market_value
    holding.last_price = price
    holding.market_value = holding.quantity * price

    db.commit()
    db.refresh(db_tx)

    return TransactionRecord(
        id=db_tx.id,
        timestamp=db_tx.timestamp,
        type=db_tx.type,
        stockId=db_tx.stock_id,
        ticker=db_tx.stock.ticker,
        quantity=float(db_tx.quantity),
        pricePerShare=float(db_tx.price_per_share),
        totalAmount=float(db_tx.total_amount)
    )

# --- Watchlist CRUD -----------------------------------------------------------

def get_watchlist(db: Session, user_id: int) -> List[WatchlistSchema]:
    entries = db.query(WatchlistEntry).filter_by(user_id=user_id).all()
    return [
        WatchlistSchema(
            stockId=e.stock_id,
            ticker=e.stock.ticker,
            lastPrice=float(e.stock.holding.last_price) if e.stock.holding else 0.0,
            dailyChangePct=0.0  # compute from price history as needed
        )
        for e in entries
    ]

def add_watchlist(db: Session, user_id: int, stock_id: int) -> WatchlistSchema:
    entry = WatchlistEntry(user_id=user_id, stock_id=stock_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return WatchlistSchema(
        stockId=entry.stock_id,
        ticker=entry.stock.ticker,
        lastPrice=float(entry.stock.holding.last_price) if entry.stock.holding else 0.0,
        dailyChangePct=0.0
    )

def remove_watchlist(db: Session, user_id: int, stock_id: int) -> None:
    db.query(WatchlistEntry).filter_by(user_id=user_id, stock_id=stock_id).delete()
    db.commit()

