# app/services/finnhub_service.py
import httpx
from app.core.config import FINNHUB_API_KEY

class FinnhubService:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url="https://finnhub.io/api/v1",
            params={"token": FINNHUB_API_KEY},
        )

    async def get_quote(self, symbol: str) -> dict:
        resp = await self.client.get("/quote", params={"symbol": symbol})
        resp.raise_for_status()
        return resp.json()
