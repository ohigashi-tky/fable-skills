"""T3 隠し受入テスト。

採点時に実行ディレクトリへコピーして実行する:
    cp benchmark/answer-keys/T3_acceptance_test.py <run-dir>/
    cd <run-dir> && python3 -m pytest T3_acceptance_test.py -v

※ 実行セッション(モデル)には絶対に見せないこと。
"""

from clock_stub import StubClock
from rate_limiter import RateLimiter


def make(max_requests=3, window=10.0):
    clock = StubClock()
    return RateLimiter(max_requests, window, clock), clock


def test_allows_under_limit():
    rl, _ = make(max_requests=3)
    assert rl.allow("u1") is True
    assert rl.allow("u1") is True
    assert rl.allow("u1") is True


def test_denies_at_limit():
    rl, _ = make(max_requests=2)
    rl.allow("u1")
    rl.allow("u1")
    assert rl.allow("u1") is False


def test_keys_are_independent():
    rl, _ = make(max_requests=1)
    assert rl.allow("u1") is True
    assert rl.allow("u2") is True
    assert rl.allow("u1") is False


def test_window_slides():
    rl, clock = make(max_requests=3, window=10.0)
    rl.allow("u1")            # t=0
    clock.advance(1)
    rl.allow("u1")            # t=1
    clock.advance(1)
    rl.allow("u1")            # t=2
    clock.advance(8)          # t=10: t=0 の記録はウィンドウ外(10 - 0 < 10 は偽)
    assert rl.allow("u1") is True
    clock.advance(0.5)        # t=10.5: 窓内は t=1, 2, 10 の3件
    assert rl.allow("u1") is False


def test_exact_window_boundary_excluded():
    rl, clock = make(max_requests=1, window=10.0)
    assert rl.allow("u1") is True   # t=0
    clock.advance(10.0)             # ちょうど window_seconds 経過
    assert rl.allow("u1") is True   # t=0 の記録は含まれない


def test_denied_requests_do_not_count():
    rl, clock = make(max_requests=2, window=10.0)
    rl.allow("u1")                   # t=0 許可
    rl.allow("u1")                   # t=0 許可
    clock.advance(5)
    assert rl.allow("u1") is False   # t=5 拒否(カウントされないこと)
    clock.advance(5.1)               # t=10.1: t=0 の2件はウィンドウ外
    # 拒否がカウントされていれば窓内に t=5 の記録が残り False になる
    assert rl.allow("u1") is True


def test_reuse_after_full_window_idle():
    rl, clock = make(max_requests=2, window=10.0)
    rl.allow("u1")
    rl.allow("u1")
    clock.advance(60)
    assert rl.allow("u1") is True
    assert rl.allow("u1") is True
    assert rl.allow("u1") is False
