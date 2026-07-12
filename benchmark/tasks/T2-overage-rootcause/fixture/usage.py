"""従量課金の使用量メーター。record() で使用量を積み上げる。"""


class UsageMeter:
    def __init__(self):
        self.total = 0.0

    def record(self, amount):
        """使用量(単位: GB)を加算する。amount は float。"""
        self.total += amount
