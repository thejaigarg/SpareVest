# API routes for transactions.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.savings.transaction import TransactionCreate, TransactionInDB
from app.crud.savings import transaction as crud_tx
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
    limit: int = Query(10, ge=1, le=100, description="Number of transctions to return."),
    offset: int = Query(0, ge=0, description="Offset for pagination."),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud_tx.get_user_transactions(db, user_id=current_user.id, limit=limit, offset=offset)

@router.post("/transfer-now")
def transfer_now(
        bank_account_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user),
):
    return crud_tx.transfer_roundup(db, user_id=current_user.id, bank_account_id=bank_account_id)