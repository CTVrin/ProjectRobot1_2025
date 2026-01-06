from typing import List, Dict, Optional
from models.product import Product, CartItem
import uuid


class ShoppingCart:

    def __init__(self):
        self.cart_id = str(uuid.uuid4())
        self.items: Dict[str, CartItem] = {}
        self._created_at = None

    def add_item(self, product: Product, quantity: int = 1) -> bool:

        if quantity <= 0:
            return False

        if product.product_id in self.items:

            self.items[product.product_id].quantity += quantity
        else:

            self.items[product.product_id] = CartItem(
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
        return True

    def remove_item(self, product_id: str, quantity: int = None) -> bool:

        if product_id not in self.items:
            return False

        if quantity is None or quantity >= self.items[product_id].quantity:

            del self.items[product_id]
        else:

            self.items[product_id].quantity -= quantity

        return True

    def update_quantity(self, product_id: str, quantity: int) -> bool:

        if product_id not in self.items or quantity <= 0:
            return False

        if quantity == 0:
            del self.items[product_id]
        else:
            self.items[product_id].quantity = quantity

        return True

    @property
    def total_price(self) -> float:

        return sum(item.total_price for item in self.items.values())

    @property
    def total_quantity(self) -> int:

        return sum(item.quantity for item in self.items.values())

    def clear(self):

        self.items.clear()

    def get_items(self) -> List[CartItem]:

        return list(self.items.values())

    def __str__(self):
        if not self.items:
            return "null"

        items_str = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(self.items.values())])
        return f"items:\n{items_str}\ntotal: ${self.total_price:.2f}"