# Pydantic schema for portfolio.py
from pydantic import BaseModel

class PortfolioSummary(BaseModel):
    id: int
    savings_goal: float
    sparevest_balance: float
    roundup_bucket: float
    percent_to_goal: float
    this_month_saved: float
    last_month_saved: float
    percent_increase: float | None = None