# backend/app/crud/market.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.models import Quote as QuoteModel
from app.schemas.market import Quote

async def upsert_quote(db: AsyncSession, quote: Quote):
    stmt = insert(QuoteModel).values(**quote.dict())
    # On conflict (symbol + timestamp), update the row instead of inserting
    stmt = stmt.on_conflict_do_update(
        index_elements=["symbol", "timestamp"],
        set_={"current": quote.current, "high": quote.high, "low": quote.low, "open": quote.open, "prev_close": quote.prev_close}
    )
    await db.execute(stmt)
    await db.commit()
