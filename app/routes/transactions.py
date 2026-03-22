from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Transaction
from ..schemas import TransactionCreate, TransactionResponse
from ..services.decision_engine import evaluate_transaction

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
