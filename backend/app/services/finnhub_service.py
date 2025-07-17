# # app/services/finnhub_service.py
# import httpx
# from app.core.config import FINNHUB_API_KEY

# class FinnhubService:
#     BASE_URL = "https://finnhub.io/api/v1"

#     def __init__(self, api_key: str = FINNHUB_API_KEY):
#         self.client = httpx.Client(base_url=self.BASE_URL, params={"token": api_key})

#     def get_quote(self, symbol: str) -> dict:
#         resp = self.client.get("/quote", params={"symbol": symbol})
#         resp.raise_for_status()
#         return resp.json()

#     def get_candles(self, symbol: str, resolution: str, _from: int, to: int) -> dict:
#         resp = self.client.get(
#             "/stock/candle",
#             params={
#                 "symbol": symbol,
#                 "resolution": resolution,
#                 "from": _from,
#                 "to": to
#             }
#         )
#         resp.raise_for_status()
#         return resp.json()
