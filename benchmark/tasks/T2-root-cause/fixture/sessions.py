"""ログインセッションの管理。ユーザー情報を TTL キャッシュに保持する。"""

from cache import TTLCache

SESSION_TTL_SECONDS = 60


class SessionStore:
    def __init__(self, clock):
        self._cache = TTLCache(clock)

    def login(self, session_id, user):
        self._cache.set(session_id, user, ttl=SESSION_TTL_SECONDS)

    def get_user(self, session_id):
        return self._cache.get(session_id)

    def greet(self, session_id):
        user = self.get_user(session_id)
        return f"ようこそ、{user['name']}さん"
