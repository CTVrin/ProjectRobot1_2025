from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class Product:
    product_id: str
    name: str
    price: float
    stock_quantity: int
    category: str = "General"
    barcode: Optional[str] = None

    def update_stock(self, quantity: int) -> bool:
        if self.stock_quantity + quantity < 0:
            return False
        self.stock_quantity += quantity
        return True

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} (Inventory: {self.stock_quantity})"


@dataclass
class CartItem:

    product: Product
    quantity: int
    unit_price: float
    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ ${self.unit_price:.2f} = ${self.total_price:.2f}"