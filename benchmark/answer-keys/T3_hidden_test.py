import pytest
from money import Money, allocate

def test_sum_invariant_basic():
    assert allocate(100, [1,1,1]) == [34,33,33]
def test_single_ratio_gets_all():
    assert allocate(100, [5]) == [100]
def test_zero_ratio_gets_zero():
    assert allocate(100, [0,1,1]) == [0,50,50]
def test_tie_break_lower_index():
    # 10 を 3等分: 各3.33..、余り1 は index0
    assert allocate(10, [1,1,1]) == [4,3,3]
def test_all_sum_equals_amount():
    for amt in [0,1,7,99,100,101,1000000,3]:
        r = allocate(amt, [1,2,3,4])
        assert sum(r) == amt
def test_zero_amount():
    assert allocate(0, [1,1,1]) == [0,0,0]
def test_negative_amount_sums():
    r = allocate(-100, [1,1,1])
    assert sum(r) == -100
    assert r == [-33,-33,-34]  # floor toward -inf: -34,-34,-34 then +1 twice to largest remainder
def test_float_ratios():
    r = allocate(100, [0.5, 0.3, 0.2])
    assert sum(r) == 100
    assert r == [50,30,20]
def test_ratios_not_normalized():
    assert allocate(100, [2,2,2]) == [34,33,33]
def test_empty_ratios_raises():
    with pytest.raises(ValueError):
        allocate(100, [])
def test_all_zero_ratios_raises():
    with pytest.raises(ValueError):
        allocate(100, [0,0])
def test_negative_ratio_raises():
    with pytest.raises(ValueError):
        allocate(100, [1,-1])
def test_non_int_amount_raises():
    with pytest.raises(TypeError):
        allocate(1.5, [1,1])
def test_money_add():
    assert Money(100,"USD").add(Money(50,"USD")) == Money(150,"USD")
def test_money_currency_mismatch():
    with pytest.raises(ValueError):
        Money(100,"USD").add(Money(50,"EUR"))
def test_money_non_int_cents():
    with pytest.raises(TypeError):
        Money(1.5,"USD")
def test_money_bad_currency():
    with pytest.raises(ValueError):
        Money(100,"US")
def test_large_distribution():
    r = allocate(100, [1]*6)
    assert sum(r) == 100 and max(r)-min(r) <= 1
