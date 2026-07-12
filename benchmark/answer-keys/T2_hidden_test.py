from usage import UsageMeter
from billing import is_overage, overage_amount

def _meter(chunks):
    m = UsageMeter()
    for c in chunks: m.record(c)
    return m

# --- 境界: 数学的にちょうど上限。float誤差で超えてはいけない(バグだと超過誤判定) ---
def test_boundary_01x3():
    assert is_overage(_meter([0.1,0.1,0.1]), 0.3) is False
def test_boundary_01_02():
    assert is_overage(_meter([0.1,0.2]), 0.3) is False
def test_boundary_11_22():
    assert is_overage(_meter([1.1,2.2]), 3.3) is False
def test_boundary_many_small():
    assert is_overage(_meter([0.1]*30), 3.0) is False
def test_boundary_amount_zero_at_limit():
    assert overage_amount(_meter([0.1,0.2]), 0.3) == 0 or abs(overage_amount(_meter([0.1,0.2]),0.3)) < 1e-9

# --- 真に超過している: True でなければならない(修正が過剰でも落ちる) ---
def test_genuinely_over():
    assert is_overage(_meter([0.1,0.1,0.1,0.1]), 0.3) is True
def test_genuinely_over_amount():
    assert overage_amount(_meter([0.5,0.5]), 0.3) > 0

# --- 明確に未満: False ---
def test_clearly_under():
    assert is_overage(_meter([0.1,0.1]), 0.3) is False
