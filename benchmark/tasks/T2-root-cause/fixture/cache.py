"""TTL 付きのシンプルなキー・バリューキャッシュ。"""


class TTLCache:
    def __init__(self, clock):
        self._clock = clock
        self._entries = {}

    def set(self, key, value, ttl=60):
        """値を保存する。ttl は秒。"""
        expires_at = self._clock.now() + ttl
        self._entries[key] = (value, expires_at)

    def get(self, key):
        """値を返す。期限切れ・未登録なら None。"""
        entry = self._entries.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if self._clock.now() > expires_at:
            del self._entries[key]
            return None
        return value
