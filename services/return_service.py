from typing import Optional, List
from models.receipt import Receipt
from models.payment import Payment, PaymentStatus
from services.sale_service import SaleService
import uuid


class ReturnService:
    """退货服务类"""

    def __init__(self, sale_service: SaleService):
        self.sale_service = sale_service
        self.return_history: List[dict] = []

    def find_receipt(self, receipt_id: str) -> Optional[Receipt]:
        """根据收据ID查找收据"""
        for receipt in self.sale_service.get_sales_history():
            if receipt.receipt_id == receipt_id:
                return receipt
        return None

    def process_return(self, receipt_id: str, returned_items: List[dict]) -> Optional[dict]:
        """处理退货"""
        receipt = self.find_receipt(receipt_id)
        if not receipt:
            return None

        # 验证退货商品
        valid_items = []
        total_refund_amount = 0.0

        for return_item in returned_items:
            product_id = return_item.get('product_id')
            quantity = return_item.get('quantity', 0)

            # 查找原始购买的商品
            original_item = None
            for item in receipt.cart_items:
                if item.product.product_id == product_id:
                    original_item = item
                    break

            if original_item and 0 < quantity <= original_item.quantity:
                valid_items.append({
                    'product': original_item.product,
                    'quantity': quantity,
                    'unit_price': original_item.unit_price,
                    'total_price': original_item.unit_price * quantity
                })
                total_refund_amount += original_item.unit_price * quantity

        if not valid_items or total_refund_amount == 0:
            return None

        # 处理退款
        refund_success = receipt.payment.refund()
        if not refund_success:
            return None

        # 更新库存
        for item in valid_items:
            self.sale_service.inventory_service.update_product_stock(
                item['product'].product_id,
                item['quantity']  # 增加库存
            )

        # 记录退货
        return_record = {
            'return_id': str(uuid.uuid4()),
            'original_receipt_id': receipt_id,
            'returned_items': valid_items,
            'refund_amount': total_refund_amount,
            'return_time': uuid.__dict__.get('uuid1')().time if hasattr(uuid, 'uuid1') else None
        }

        self.return_history.append(return_record)

        return return_record

    def get_return_history(self) -> List[dict]:
        """获取退货历史"""
        return self.return_history
