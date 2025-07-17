# API routes for portfolio.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.savings.portfolio import PortfolioSummary, PortfolioGoalUpdate
from app.crud.savings.portfolio import build_portfolio_summary

router = APIRouter(
    prefix = "/portfolio",
    tags=["portfolio"],
)

@router.get("/summary", response_model = PortfolioSummary)
def summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return build_portfolio_summary(current_user)

@router.patch("/goal", response_model=PortfolioSummary)
def update_savings_goal(
    data: PortfolioGoalUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    portfolio = current_user.portfolio
    portfolio.savings_goal = data.savings_goal
    db.commit()
    db.refresh(portfolio)

    return build_portfolio_summary(current_user)