"""売上データの取得。接続エラー時はリトライする。"""

import time

import api_client


def fetch_sales(config):
    attempt = 0
    while True:
        try:
            return api_client.get_sales(timeout=config["timeout"])
        except ConnectionError:
            attempt += 1
            if attempt > config["max_retries"]:
                raise
            time.sleep(2 ** attempt)
