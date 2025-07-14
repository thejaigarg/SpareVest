# backend/app/api/market.py
from fastapi import APIRouter, Depends
from app.services.finnhub_service import FinnhubService

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/quote/{symbol}")
async def read_quote(symbol: str, fh: FinnhubService = Depends()):
    data = await fh.get_quote(symbol)
    return {
        "symbol": symbol,
        "current": data["c"],
        "high": data["h"],
        "low":  data["l"],
        "open": data["o"],
        "prev": data["pc"],
    }
