"""従量課金の使用量メーター。record() で使用量を積み上げる。"""

_SCALE = 1_000_000  # マイクロGB。float 誤差を避けるため内部は整数で保持する。


class UsageMeter:
    def __init__(self):
        self._micro = 0

    def record(self, amount):
        """使用量(単位: GB)を加算する。amount は float。"""
        self._micro += round(amount * _SCALE)

    @property
    def total(self):
        return self._micro / _SCALE
