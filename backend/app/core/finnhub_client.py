import finnhub
from app.core.config import FINNHUB_API_KEY

_client = finnhub.Client(api_key=FINNHUB_API_KEY)

Client = finnhub.Client    # <— export the class so other modules don’t need to import finnhub directly

def get_finnhub_client() -> Client:
    return _client
