from clock import FakeClock
from sessions import SessionStore


def test_active_session_greets_user():
    clock = FakeClock()
    store = SessionStore(clock)
    store.login("s1", {"name": "田中"})

    clock.advance(30_000)  # 30秒経過(TTL 60秒の半分)

    assert store.greet("s1") == "ようこそ、田中さん"


def test_expired_session_returns_none():
    clock = FakeClock()
    store = SessionStore(clock)
    store.login("s1", {"name": "田中"})

    clock.advance(120_000)  # 120秒経過(TTL 60秒を超過)

    assert store.get_user("s1") is None
