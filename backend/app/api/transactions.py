# API routes for transactions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate, TransactionInDB
from app.crud import transaction as crud_tx
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

@router.post("/", response_model=TransactionInDB)
def add_transaction(
    tx: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_tx.create_transaction(db, user_id=current_user.id, tx=tx)

@router.get("/", response_model=list[TransactionInDB])
def list_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_tx.get_user_transactions(db, user_id=current_user.id)