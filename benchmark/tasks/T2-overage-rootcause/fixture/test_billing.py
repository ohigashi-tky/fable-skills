from usage import UsageMeter
from billing import is_overage


def test_exact_limit_is_not_overage():
    meter = UsageMeter()
    for _ in range(3):
        meter.record(0.1)     # 0.1GB を3回 = ちょうど0.3GB
    assert is_overage(meter, 0.3) is False
