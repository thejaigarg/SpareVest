# # app/api/invest/holdings.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from typing import List

# from app.schemas.invest. import HoldingsResponse
# from app.crud.invest import stocks as crud_stocks
# from app.core.database import get_db
# from app.api.deps import get_current_user

# router = APIRouter(prefix="/holdings", tags=["holdings"])

# @router.get("/", response_model=HoldingsResponse)
# def get_holdings(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user),
# ):
#     return crud_stocks.get_user_holdings(db, user_id=current_user.id)
