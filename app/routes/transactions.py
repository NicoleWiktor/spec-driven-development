from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Transaction
from ..schemas import TransactionCreate, TransactionResponse
from ..services.decision_engine import evaluate_transaction

router = APIRouter(tags=["transactions"])
ALLOWED_DECISIONS = {"approved", "review", "rejected"}


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
) -> Transaction:
    decision, reasons = evaluate_transaction(payload)

    transaction = Transaction(
        account_id=payload.account_id,
        amount=payload.amount,
        country=payload.country,
        available_balance=payload.available_balance,
        account_status=payload.account_status,
        transaction_type=payload.transaction_type,
        new_payee=payload.new_payee,
        decision=decision,
        reasons=reasons,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/transactions", response_model=list[TransactionResponse])
def list_transactions(
    decision: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Transaction]:
    if decision is not None and decision not in ALLOWED_DECISIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid decision filter. Allowed values: approved, review, rejected.",
        )

    query = db.query(Transaction)
    if decision is not None:
        query = query.filter(Transaction.decision == decision)
    return query.all()


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
) -> Transaction:
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found.",
        )
    return transaction
