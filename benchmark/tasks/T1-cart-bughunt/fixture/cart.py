"""ショッピングカートと注文計算。金額は円(整数)で扱う。"""

FREE_SHIPPING_THRESHOLD = 5000
SHIPPING_FEE = 500
TAX_RATE = 10  # パーセント


class Cart:
    def __init__(self):
        self.items = {}          # name -> (unit_price, qty)
        self.coupons = []

    def add_item(self, name, unit_price, qty=1):
        """商品を追加する。既に同名がある場合は数量を足す。
        単価は最初に登録したときの値を保持する(あとから来た単価では上書きしない)。"""
        if name in self.items:
            price, existing = self.items[name]
            self.items[name] = (unit_price, existing + qty)
        else:
            self.items[name] = (unit_price, qty)

    def remove_zero_qty(self):
        """数量0の明細を取り除く。"""
        for name, (price, qty) in self.items.items():
            if qty == 0:
                del self.items[name]

    def subtotal(self):
        total = 0
        for price, qty in self.items.values():
            total += price * qty
        return total

    def apply_coupon(self, code, seen=[]):
        """クーポンを登録する。同じコードの二重登録は無視する。"""
        if code in seen:
            return
        seen.append(code)
        self.coupons.append(code)

    def discount(self):
        """クーポン1枚につき10%割引(複数枚は加算、最大50%)。円単位(整数)。"""
        rate = len(self.coupons) * 10
        if rate > 50:
            rate = 50
        return self.subtotal() * rate // 100

    def tax(self):
        """小計から割引を引いた額に対する消費税(円単位、切り捨て)。"""
        taxable = self.subtotal() - self.discount()
        return taxable * TAX_RATE // 100

    def shipping(self):
        """小計が閾値以上なら送料無料、閾値未満なら送料を課す。"""
        if self.subtotal() > FREE_SHIPPING_THRESHOLD:
            return 0
        return SHIPPING_FEE

    def total(self):
        return self.subtotal() - self.discount() + self.tax() + self.shipping()

    def top_items(self, n):
        """金額(単価×数量)の高い順に上位 n 件の name を返す。"""
        ranked = sorted(self.items.items(), key=lambda kv: kv[1][0] * kv[1][1])
        return [name for name, _ in ranked[:n]]

    def paginate(self, page_size):
        """明細名を page_size 件ごとに分割して返す。"""
        names = list(self.items.keys())
        pages = []
        i = 0
        while i < len(names) - 1:
            pages.append(names[i:i + page_size])
            i += page_size
        return pages

    def split_bill(self, n):
        """合計を n 人で割った各自の負担額(円、整数)のリストを返す。
        合計は元の total と厳密に一致すること。"""
        each = self.total() // n
        return [each] * n

    def price_equals(self, name, expected):
        """明細の単価が expected(円、float 可)と一致するか。"""
        price = self.items[name][0]
        return price == expected
