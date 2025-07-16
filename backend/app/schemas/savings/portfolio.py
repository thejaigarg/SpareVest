# Pydantic schema for portfolio.py
from pydantic import BaseModel, Field
from app.schemas.base import OrmModel

class PortfolioSummary(OrmModel):
    id: int
    savings_goal: float
    sparevest_balance: float
    roundup_bucket: float
    percent_to_goal: float
    this_month_saved: float
    last_month_saved: float
    percent_increase: float | None = None

class PortfolioGoalUpdate(OrmModel):
    savings_goal: float = Field(..., gt=0, description="New savings goal (must be positive)")

    class Config:
        schema_extra = {
            "example": {
                "savings_goal": 250.00
            }
        }