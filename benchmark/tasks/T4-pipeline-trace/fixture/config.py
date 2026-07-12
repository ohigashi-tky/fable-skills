"""設定。デフォルト → 環境変数の順で解決する。"""

import os

DEFAULTS = {"mode": "safe", "workers": 4}


def resolve(key):
    env_key = "APP_" + key.upper()
    if os.environ.get(env_key):     # 空文字は無視してデフォルトにフォールバック
        raw = os.environ[env_key]
        if type(DEFAULTS[key]) is int:
            return int(raw)
        return raw
    return DEFAULTS[key]
