from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid


class PaymentMethod(Enum):
    """支付方式枚举"""
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    MOBILE_PAYMENT = "mobile_payment"


class PaymentStatus(Enum):
    """支付状态枚举"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass
class Payment:

    payment_id: str
    amount: float
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    created_at: datetime = None
    processed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def process_payment(self) -> bool:

        if self.status != PaymentStatus.PENDING:
            return False

        # 模拟支付处理
        if self.amount > 0:
            self.status = PaymentStatus.SUCCESS
            self.transaction_id = f"TXN{str(uuid.uuid4())[:8].upper()}"
            self.processed_at = datetime.now()
            return True
        return False

    def refund(self) -> bool:

        if self.status == PaymentStatus.SUCCESS:
            self.status = PaymentStatus.REFUNDED
            return True
        return False

    def __str__(self):
        return f"PaymentID: {self.payment_id} | Amount: ${self.amount:.2f} | Method: {self.method.value} | Status: {self.status.value}"