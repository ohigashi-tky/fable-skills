"""テスト用の時刻スタブ。"""


class StubClock:
    def __init__(self, start=1_700_000_000.0):
        self._now = float(start)

    def now(self):
        return self._now

    def advance(self, seconds):
        self._now += seconds
