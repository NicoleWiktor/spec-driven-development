from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Transaction
from ..schemas import TransactionCreate, TransactionResponse

router = APIRouter(tags=["transactions"])


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
) -> Transaction:
    if payload.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="amount must be greater than 0",
        )

    transaction = Transaction(
        account_id=payload.account_id,
        amount=payload.amount,
        country=payload.country,
        available_balance=payload.available_balance,
        account_status=payload.account_status,
        transaction_type=payload.transaction_type,
        new_payee=payload.new_payee,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
