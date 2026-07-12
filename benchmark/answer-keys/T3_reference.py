# リファレンス実装(正解キー検証用。実行役には渡さない)
from decimal import Decimal
from math import floor


class Money:
    __slots__ = ("cents", "currency")

    def __init__(self, cents, currency):
        if type(cents) is not int:
            raise TypeError("cents must be int")
        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError("currency must be a 3-letter code")
        self.cents = cents
        self.currency = currency

    def _guard(self, other):
        if not isinstance(other, Money):
            raise TypeError("operand must be Money")
        if other.currency != self.currency:
            raise ValueError("currency mismatch")

    def add(self, other):
        self._guard(other)
        return Money(self.cents + other.cents, self.currency)

    def subtract(self, other):
        self._guard(other)
        return Money(self.cents - other.cents, self.currency)

    def __eq__(self, other):
        return isinstance(other, Money) and self.cents == other.cents and self.currency == other.currency

    def __repr__(self):
        return f"Money({self.cents}, {self.currency!r})"


def allocate(amount_cents, ratios):
    if type(amount_cents) is not int:
        raise TypeError("amount_cents must be int")
    if not ratios:
        raise ValueError("ratios must be non-empty")
    if any(r < 0 for r in ratios):
        raise ValueError("ratios must be non-negative")
    total = sum(Decimal(str(r)) for r in ratios)
    if total == 0:
        raise ValueError("ratios must not all be zero")
    # 正確な有理分配 → 各要素は floor、余りセントを剰余の大きい順(同点は index 昇順)に +1(負なら -1)
    amt = Decimal(amount_cents)
    exact = [amt * Decimal(str(r)) / total for r in ratios]
    floors = [floor(e) for e in exact]  # floor toward -inf
    remainder = amount_cents - sum(floors)
    # remainder は 0..len-1 の範囲(負の総額でも floor toward -inf なので remainder >= 0)
    fracs = sorted(range(len(ratios)), key=lambda i: (-(exact[i] - floors[i]), i))
    result = list(floors)
    for k in range(remainder):
        result[fracs[k]] += 1
    return result
