# app/crud/invest/price_history.py

from datetime import datetime, timedelta
from typing import List, Optional

import yfinance as yf
from sqlalchemy.orm import Session

from app.models.invest.price_history import PriceHistory
from app.models.invest.stock import Stock
from app.schemas.invest import price_history as price_history_schema


def get_or_refresh_price_history(
    db: Session,
    stock_id: int,
    days_to_fetch: int = 30,
) -> List[price_history_schema.PricePointInDB]:
    """Return cached history up through yesterday or fetch + cache the last `days_to_fetch` days."""
    # 1) Cache check
    latest: Optional[PriceHistory] = (
        db.query(PriceHistory)
          .filter(PriceHistory.stock_id == stock_id)
          .order_by(PriceHistory.date.desc())
          .first()
    )
    today = datetime.utcnow().date()
    if latest and latest.date >= today - timedelta(days=1):
        cached = (
            db.query(PriceHistory)
              .filter(PriceHistory.stock_id == stock_id)
              .order_by(PriceHistory.date)
              .all()
        )
        return [price_history_schema.PricePointInDB.from_orm(r) for r in cached]

    # 2) Fetch via yfinance
    stock: Optional[Stock] = db.get(Stock, stock_id)
    if not stock:
        return []

    end_dt = datetime.utcnow()
    start_dt = end_dt - timedelta(days=days_to_fetch)

    df = yf.Ticker(stock.ticker).history(
        start=start_dt,
        end=end_dt,
        interval="1d",
        auto_adjust=False,
        actions=False,
    )

    points: List[PriceHistory] = []
    for ts, row in df.iterrows():
        dt = ts.date()
        openp = float(row["Open"])
        highp = float(row["High"])
        lowp  = float(row["Low"])
        closep= float(row["Close"])
        vol   = int(row["Volume"])

        ph: Optional[PriceHistory] = (
            db.query(PriceHistory)
              .filter_by(stock_id=stock_id, date=dt)
              .first()
        )
        if ph:
            ph.open_price   = openp
            ph.high_price   = highp
            ph.low_price    = lowp
            ph.close_price  = closep
            ph.volume       = vol
        else:
            ph = PriceHistory(
                stock_id    = stock_id,
                date        = dt,
                open_price  = openp,
                high_price  = highp,
                low_price   = lowp,
                close_price = closep,
                volume      = vol,
            )
            db.add(ph)

        points.append(ph)

    db.commit()
    points.sort(key=lambda p: p.date)
    return [price_history_schema.PricePointInDB.from_orm(p) for p in points]


def create_price_point(
    db: Session,
    price_in: price_history_schema.PricePointCreate,
) -> price_history_schema.PricePointInDB:
    db_point = PriceHistory(
        stock_id    = price_in.stock_id,
        date        = price_in.date,
        open_price  = price_in.open_price,
        high_price  = price_in.high_price,
        low_price   = price_in.low_price,
        close_price = price_in.close_price,
        volume      = price_in.volume,
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return price_history_schema.PricePointInDB.from_orm(db_point)


def get_price_history(
    db: Session,
    stock_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[price_history_schema.PricePointInDB]:
    rows = (
        db.query(PriceHistory)
          .filter(PriceHistory.stock_id == stock_id)
          .order_by(PriceHistory.date)
          .offset(skip)
          .limit(limit)
          .all()
    )
    return [price_history_schema.PricePointInDB.from_orm(r) for r in rows]


def delete_price_point(
    db: Session,
    point_id: int,
) -> bool:
    p = db.query(PriceHistory).filter(PriceHistory.id == point_id).first()
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True
