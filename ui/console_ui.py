from services.inventory_service import InventoryService
from services.sale_service import SaleService
from services.return_service import ReturnService
from models.payment import PaymentMethod
import os


class ConsoleUI:
    """控制台用户界面"""

    def __init__(self):
        self.inventory_service = InventoryService()
        self.sale_service = SaleService(self.inventory_service)
        self.return_service = ReturnService(self.sale_service)
        self.current_cart = None

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """显示主菜单"""
        print("=" * 50)
        print("           Supermarket POS System")
        print("=" * 50)
        print("1. Start New Sale")
        print("2. Handle Returns")
        print("3. Check product inventory")
        print("4. View Sales History")
        print("5. View return history")
        print("6. Exit")
        print("=" * 50)

    def display_products(self):
        """显示商品列表"""
        products = self.inventory_service.get_all_products()
        print("\nProduct Inventory:")
        print("-" * 60)
        for i, product in enumerate(products, 1):
            print(f"{i}. {product}")
        print("-" * 60)

    def start_new_sale(self):
        """开始新销售"""
        self.current_cart = self.sale_service.create_new_sale()
        print("\nStart a new sale...")

        while True:
            self.clear_screen()
            print("Current shopping cart:")
            print(self.current_cart)
            print("\nOptions:")
            print("1. Add Product")
            print("2. Complete the sale")
            print("3. Cancel Sale")

            choice = input("\nPlease select an action: ")

            if choice == "1":
                self.add_product_to_sale()
            elif choice == "2":
                self.complete_sale()
                break
            elif choice == "3":
                print("The sale has been canceled")
                self.current_cart = None
                break
            else:
                print("Invalid selection, please enter again")

    def add_product_to_sale(self):
        """添加商品到销售"""
        self.display_products()

        try:
            product_num = int(input("\nPlease enter the ProductID: "))
            products = self.inventory_service.get_all_products()

            if 1 <= product_num <= len(products):
                product = products[product_num - 1]
                quantity = int(input("Please enter the quantity: "))

                if quantity > 0:
                    success = self.sale_service.add_product_to_sale(
                        self.current_cart, product.product_id, quantity
                    )
                    if success:
                        print(f"Added {product.name} x{quantity}")
                    else:
                        print("Failed to add, insufficient stock")
                else:
                    print("The quantity must be greater than 0")
            else:
                print("Invalid productID")
        except ValueError:
            print("Please enter a valid number")

        input("\nPress Enter to continue...")

    def complete_sale(self):
        """完成销售"""
        if not self.current_cart or self.current_cart.total_quantity == 0:
            print("The shopping cart is empty, unable to complete the purchase.")
            return

        print("\nChoose a payment method:")
        print("1. Cash")
        print("2. Credit card")
        print("3. Debit Card")
        print("4. Mobile payment")

        payment_methods = {
            "1": PaymentMethod.CASH,
            "2": PaymentMethod.CREDIT_CARD,
            "3": PaymentMethod.DEBIT_CARD,
            "4": PaymentMethod.MOBILE_PAYMENT
        }

        choice = input("Please choose a payment method:")
        payment_method = payment_methods.get(choice)

        if payment_method:
            receipt = self.sale_service.process_payment(self.current_cart, payment_method)
            if receipt:
                print("\nSale completed!")
                print(receipt)
            else:
                print("Payment processing failed")
        else:
            print("Invalid payment method")

        self.current_cart = None
        input("\nPress Enter to return to the main menu...")

    def process_return(self):
        """处理退货"""
        print("\nHandle Returns")
        receipt_id = input("Please enter the receipt ID: ")

        receipt = self.return_service.find_receipt(receipt_id)
        if not receipt:
            print("No corresponding sales record found")
            return

        print("\nFind sales records:")
        print(receipt)

        returned_items = []
        print("\nPlease enter the item you want to return:")

        for i, item in enumerate(receipt.cart_items, 1):
            print(f"{i}. {item.product.name} - Purchase Quantity: {item.quantity}")

        while True:
            try:
                item_num = int(input("\nPlease enter the product code (enter 0 to finish): "))
                if item_num == 0:
                    break
                if 1 <= item_num <= len(receipt.cart_items):
                    quantity = int(input("Please enter the return quantity: "))
                    original_item = receipt.cart_items[item_num - 1]

                    if 0 < quantity <= original_item.quantity:
                        returned_items.append({
                            'product_id': original_item.product.product_id,
                            'quantity': quantity
                        })
                        print(f"Added {original_item.product.name} x{quantity} to return list")
                    else:
                        print("Invalid return quantity")
                else:
                    print("Invalid product number")
            except ValueError:
                print("Please enter a valid number")

        if returned_items:
            return_result = self.return_service.process_return(receipt_id, returned_items)
            if return_result:
                print("\nReturn processed successfully!")
                print(f"Refund Amount: ${return_result['refund_amount']:.2f}")
                print(f"Return ID: {return_result['return_id']}")
            else:
                print("Return processing failed")
        else:
            print("There are no items to return")

        input("\nPress Enter to continue...")

    def view_sales_history(self):
        """查看销售历史"""
        sales = self.sale_service.get_sales_history()
        print("\nSales History:")
        print("-" * 80)
        for i, sale in enumerate(sales, 1):
            print(
                f"{i}. Receipt ID: {sale.receipt_id} | Time: {sale.created_at.strftime('%Y-%m-%d %H:%M')} | amount: ${sale.final_amount:.2f}")
        print("-" * 80)
        input("\nPress Enter to continue...")

    def view_return_history(self):
        """查看退货历史"""
        returns = self.return_service.get_return_history()
        print("\nReturn History:")
        print("-" * 80)
        for i, return_record in enumerate(returns, 1):
            print(
                f"{i}. Return ID: {return_record['return_id']} | Original Receipt ID: {return_record['original_receipt_id']} | Refund Amount: ${return_record['refund_amount']:.2f}")
        print("-" * 80)
        input("\nPress Enter to continue...")

    def run(self):
        """运行主程序"""
        while True:
            self.clear_screen()
            self.display_menu()

            choice = input("please chose : ")

            if choice == "1":
                self.start_new_sale()
            elif choice == "2":
                self.process_return()
            elif choice == "3":
                self.clear_screen()
                self.display_products()
                input("\npress enter to continue...")
            elif choice == "4":
                self.clear_screen()
                self.view_sales_history()
            elif choice == "5":
                self.clear_screen()
                self.view_return_history()
            elif choice == "6":
                print("Thank you for using the supermarket POS system. Goodbye!")
                break
            else:
                print("Invalid selection, please enter again")
                input("press enter to continue...")