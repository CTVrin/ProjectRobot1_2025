from dataclasses import dataclass
from typing import List
from datetime import datetime
from models.product import CartItem
from models.payment import Payment
import uuid


@dataclass
class Receipt:
    receipt_id: str
    cart_items: List[CartItem]
    payment: Payment
    total_amount: float
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    final_amount: float = 0.0
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.final_amount == 0.0:
            self.final_amount = self.total_amount + self.tax_amount - self.discount_amount

    def generate_receipt_text(self) -> str:
        receipt_lines = []
        receipt_lines.append("=" * 40)
        receipt_lines.append("           Supermarket receipt")
        receipt_lines.append("=" * 40)
        receipt_lines.append(f"receiptID: {self.receipt_id}")
        receipt_lines.append(f"time: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append("-" * 40)

        receipt_lines.append("Product Details:")
        for i, item in enumerate(self.cart_items, 1):
            receipt_lines.append(f"{i}. {item.product.name} x{item.quantity} @ ${item.unit_price:.2f}")

        receipt_lines.append("-" * 40)
        receipt_lines.append(f"Total: ${self.total_amount:.2f}")
        if self.tax_amount > 0:
            receipt_lines.append(f"Tax: ${self.tax_amount:.2f}")
        if self.discount_amount > 0:
            receipt_lines.append(f"Discount: -${self.discount_amount:.2f}")
        receipt_lines.append(f"Amount Paid: ${self.final_amount:.2f}")
        receipt_lines.append(f"Payment Method: {self.payment.method.value}")
        receipt_lines.append(f"PaymentID: {self.payment.transaction_id}")
        receipt_lines.append("=" * 40)
        receipt_lines.append("        Thank you for your patronage, and we look forward to seeing you again!")
        receipt_lines.append("=" * 40)

        return "\n".join(receipt_lines)

    def __str__(self):
        return self.generate_receipt_text()