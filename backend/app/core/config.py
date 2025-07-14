# backend/app/core/config.py
from dotenv import load_dotenv, find_dotenv
import os

# Load .env in development only (no-op if no .env file)
load_dotenv(find_dotenv())

DATABASE_URL     = os.getenv("DATABASE_URL")
TEST_DATABASE_URL= os.getenv("TEST_DATABASE_URL")
SECRET_KEY       = os.getenv("SECRET_KEY")
GMAIL_USER       = os.getenv("GMAIL_USER")
GMAIL_PASS       = os.getenv("GMAIL_PASS")
FRONTEND_URL     = os.getenv("FRONTEND_URL", "http://localhost:80")
FINNHUB_API_KEY  = os.getenv("FINNHUB_API_KEY")

# Optional sanity checks in dev:
if not DATABASE_URL or not SECRET_KEY:
    raise RuntimeError("Missing required environment variables")
if not FINNHUB_API_KEY:
    raise RuntimeError("Missing environment variable: FINNHUB_API_KEY")