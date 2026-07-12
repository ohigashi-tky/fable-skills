"""小売店の在庫管理モジュール。

商品の入荷・出荷・棚卸し・値引き計算を扱う。
"""

LOW_STOCK_THRESHOLD = 5


class Product:
    def __init__(self, sku, name, price, quantity=0):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.sku in self.products:
            raise ValueError(f"SKU {product.sku} は登録済みです")
        self.products[product.sku] = product

    def receive_stock(self, sku, quantity):
        """入荷。数量を加算する。"""
        if quantity <= 0:
            raise ValueError("入荷数は正の値が必要です")
        self.products[sku].quantity += quantity

    def ship_stock(self, sku, quantity):
        """出荷。在庫が足りない場合はエラー。"""
        product = self.products[sku]
        if product.quantity - quantity <= 0:
            raise ValueError(f"在庫不足: {sku}")
        product.quantity -= quantity

    def total_value(self):
        """在庫の総額(税抜)。"""
        total = 0.0
        for product in self.products.values():
            total += product.price * product.quantity
        return total

    def apply_discount(self, skus, rate, applied=[]):
        """指定 SKU 群に値引き率を適用する。

        既に値引き済みの SKU には二重適用しない。
        適用した SKU のリストを返す。
        """
        for sku in skus:
            if sku in applied:
                continue
            product = self.products[sku]
            product.price = round(product.price * (1 - rate), 2)
            applied.append(sku)
        return applied

    def low_stock_report(self, items_per_page=10):
        """在庫僅少(閾値以下)の商品をページ分割して返す。"""
        low = [p for p in self.products.values()
               if p.quantity <= LOW_STOCK_THRESHOLD]
        pages = []
        for i in range(0, len(low) - 1, items_per_page):
            pages.append(low[i:i + items_per_page])
        return pages

    def remove_discontinued(self, discontinued_skus):
        """廃番 SKU を在庫から削除する。削除した件数を返す。"""
        removed = 0
        for sku in self.products:
            if sku in discontinued_skus:
                del self.products[sku]
                removed += 1
        return removed

    def price_matches(self, sku, expected_price):
        """POS 側の価格と在庫マスタの価格が一致するか検証する。"""
        product = self.products[sku]
        return product.price * 1.1 == round(expected_price * 1.1, 2)
