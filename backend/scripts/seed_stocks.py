# backend/scripts/seed_stocks.py

import os
import time
import httpx
import sys

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import DATABASE_URL
from app.models import Stock

# --- CONFIGURATION ---
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    print("❌ Please set FINNHUB_API_KEY in your environment and rerun.")
    sys.exit(1)

FINNHUB_BASE = "https://finnhub.io/api/v1"

# --- DATABASE SETUP (sync) ---
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- FETCH SYMBOLS ---
def fetch_us_symbols():
    t0 = time.time()
    url = f"{FINNHUB_BASE}/stock/symbol"
    params = {"exchange": "US", "token": FINNHUB_API_KEY}
    with httpx.Client(timeout=60.0) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    print(f"Fetched {len(data)} symbols in {time.time() - t0:.2f}s")
    return data

# --- MAIN SEED LOGIC ---
def main():
    overall_start = time.time()

    symbols = fetch_us_symbols()

    # 1) Load existing tickers in one go
    t1 = time.time()
    session = SessionLocal()
    existing = {row[0] for row in session.query(Stock.ticker).all()}
    print(f"Loaded {len(existing)} existing tickers in {time.time() - t1:.2f}s")

    # 2) Prepare list of new entries
    t2 = time.time()
    new_entries = []
    for item in symbols:
        ticker   = item.get("symbol")
        name     = item.get("description", "").strip()
        currency = item.get("currency", "USD")
        if ticker and name and ticker not in existing:
            new_entries.append({
                "ticker":   ticker,
                "name":     name,
                "currency": currency,
            })
    print(f"Prepared {len(new_entries)} new entries in {time.time() - t2:.2f}s")

    # 3) Bulk insert all at once
    if new_entries:
        t3 = time.time()
        try:
            session.bulk_insert_mappings(Stock, new_entries)
            session.commit()
            print(f"Inserted {len(new_entries)} rows in {time.time() - t3:.2f}s")
        except SQLAlchemyError as e:
            session.rollback()
            print("❌ Insert failed:", e)
            sys.exit(1)

    session.close()
    print(f"✅ Done in {time.time() - overall_start:.2f}s")

if __name__ == "__main__":
    main()
