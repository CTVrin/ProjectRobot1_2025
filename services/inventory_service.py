from typing import Dict, List, Optional
from models.product import Product


class InventoryService:

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self._initialize_sample_products()

    def _initialize_sample_products(self):
        sample_products = [
            Product("P001", "可口可乐", 3.5, 100, "饮料", "1234567890123"),
            Product("P002", "薯片", 8.5, 50, "零食", "1234567890124"),
            Product("P003", "牛奶", 12.0, 30, "乳制品", "1234567890125"),
            Product("P004", "面包", 6.0, 40, "食品", "1234567890126"),
            Product("P005", "矿泉水", 2.0, 200, "饮料", "1234567890127"),
        ]

        for product in sample_products:
            self.products[product.product_id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def get_product_by_barcode(self, barcode: str) -> Optional[Product]:
        for product in self.products.values():
            if product.barcode == barcode:
                return product
        return None

    def search_products(self, keyword: str) -> List[Product]:
        keyword = keyword.lower()
        results = []
        for product in self.products.values():
            if keyword in product.name.lower() or keyword in product.category.lower():
                results.append(product)
        return results

    def update_product_stock(self, product_id: str, quantity: int) -> bool:
        product = self.get_product(product_id)
        if product:
            return product.update_stock(quantity)
        return False

    def get_all_products(self) -> List[Product]:
        return list(self.products.values())

    def add_product(self, product: Product) -> bool:
        if product.product_id in self.products:
            return False
        self.products[product.product_id] = product
        return True
