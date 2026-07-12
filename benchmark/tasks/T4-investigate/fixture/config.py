"""設定の読み込み。

デフォルト値 → 設定ファイル → 環境変数の順で重ねる。
"""

import json
import os

DEFAULTS = {
    "timeout": 30,
    "max_retries": 3,
    "locale": "en",
    "output_dir": "./out",
}

ENV_PREFIX = "RPT_"

CONFIG_FILE = "report.json"


def load_config():
    config = dict(DEFAULTS)

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config.update(json.load(f))

    for key in DEFAULTS:
        env_key = ENV_PREFIX + key.upper()
        if env_key in os.environ:
            raw = os.environ[env_key]
            if isinstance(DEFAULTS[key], int):
                config[key] = int(raw)
            else:
                config[key] = raw

    return config
