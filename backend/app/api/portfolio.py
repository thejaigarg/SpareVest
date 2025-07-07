# API routes for portfolio.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.portfolio import PortfolioSummary

router = APIRouter(
    prefix = "/portfolio",
    tags=["portfolio"],
)

@router.get("/summary", response_model = PortfolioSummary)
def summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    portfolio = current_user.portfolio
    #current stats
    balance = portfolio.sparevest_balance
    goal = portfolio.savings_goal
    roundup_bucket = portfolio.roundup_bucket

    percent = (roundup_bucket/goal * 100) if goal else 0.0

    #Date calculations
    now = datetime.utcnow()
    this_mo_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_mo_start = this_mo_start-relativedelta(months=1)
    last_mo_end = this_mo_start-timedelta(seconds=1)

    #Transction sum helpers
    def sum_transactions(q):
        return sum(t.amount for t in q)
    
    this_month = [
        t for t in current_user.transactions
        if t.type == "deposit_to_app" and t.created_at >= this_mo_start
    ]

    last_month = [
        t for t in current_user.transactions
        if t.type == "deposit_to_app" and last_mo_start <= t.created_at < this_mo_start
    ]

    this_month_saved = sum_transactions(this_month)
    last_month_saved = sum_transactions(last_month)

    percent_increase = None
    if last_month_saved:
        percent_increase=(this_month_saved-last_month_saved)/last_month_saved
    elif last_month_saved == 0 and this_month_saved>0:
        percent_increase = 1.0

    return PortfolioSummary(
        id=portfolio.id,
        savings_goal=goal,
        sparevest_balance=balance,
        roundup_bucket=roundup_bucket,
        percent_to_goal=percent,
        this_month_saved=this_month_saved,
        last_month_saved=last_month_saved,
        percent_increase=percent_increase
    )