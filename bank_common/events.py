from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


TxnType = Literal["deposit", "withdraw", "transfer", "wealth_buy"]


class AccountingEvent(BaseModel):
    event_id: str
    txn_id: str
    txn_type: TxnType
    amount_cents: int
    currency: str = "USD"
    debit_account_no: Optional[str] = None
    credit_account_no: Optional[str] = None
    customer_id: Optional[int] = None
    txn_code: str = ""
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
