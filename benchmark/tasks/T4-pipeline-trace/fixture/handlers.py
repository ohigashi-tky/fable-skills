"""売上ハンドラ群。同じ名前で複数登録されることがある。"""

from registry import register
from retry import retry
from cache import memoize

_calls = {"flaky": 0}


@register("normalize")
def normalize_v1(x):
    return x.strip().lower()


@register("normalize")
def normalize_v2(x):
    return x.strip().upper()


@register("compute")
@memoize
def compute(n):
    return n * n


@retry(times=2)
def flaky(fail_until):
    _calls["flaky"] += 1
    if _calls["flaky"] < fail_until:
        raise ValueError("not yet")
    return _calls["flaky"]
