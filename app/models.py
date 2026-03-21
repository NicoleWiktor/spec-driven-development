from decimal import Decimal

from sqlalchemy import Boolean, Integer, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    country: Mapped[str] = mapped_column(String(2))
    available_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    account_status: Mapped[str] = mapped_column(String(32))
    transaction_type: Mapped[str] = mapped_column(String(32))
    new_payee: Mapped[bool] = mapped_column(Boolean, default=False)
    decision: Mapped[str] = mapped_column(String(32), default="pending")
    reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
