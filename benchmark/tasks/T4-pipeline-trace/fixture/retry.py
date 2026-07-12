"""リトライ用デコレータ。"""

import functools


def retry(times, catch=(ValueError,)):
    """失敗したら最大 times 回まで追加で再実行する。
    最初の実行 + times 回のリトライ = 最大 times+1 回試行する。"""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except catch as e:
                    attempts += 1
                    if attempts > times:
                        raise
        return wrapper
    return deco
