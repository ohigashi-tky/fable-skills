"""時刻ソース。テストで差し替えられるように抽象化してある。"""

import time


class SystemClock:
    """現在時刻をエポックからのミリ秒で返す。"""

    def now(self):
        return int(time.time() * 1000)


class FakeClock:
    """テスト用。advance() で時間を進められる。単位はミリ秒。"""

    def __init__(self, start=1_700_000_000_000):
        self._now = start

    def now(self):
        return self._now

    def advance(self, ms):
        self._now += ms
