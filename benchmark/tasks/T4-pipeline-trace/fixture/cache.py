"""結果キャッシュ用デコレータ。引数をキーにして戻り値を保存する。"""

import functools


def memoize(fn):
    store = {}

    @functools.wraps(fn)
    def wrapper(*args):
        key = args
        if key in store:
            return store[key]
        result = fn(*args)   # 例外はキャッシュしない(伝播する)
        store[key] = result
        return result
    return wrapper
