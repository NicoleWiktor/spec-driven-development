from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    account_id: str
    amount: Decimal
    country: str
    available_balance: Decimal
    account_status: str
    transaction_type: str
    new_payee: bool


class TransactionResponse(BaseModel):
    id: int
    decision: str
    reasons: list[str]

    model_config = ConfigDict(from_attributes=True)


class TransactionSummaryResponse(BaseModel):
    total: int
    approved: int
    review: int
    rejected: int
