# 依頼

このリポジトリに API のレートリミッターを実装してください。

## 仕様

`rate_limiter.py` に `RateLimiter` クラスを実装する:

- `RateLimiter(max_requests, window_seconds, clock)` — `clock` は `now()` でエポック秒(float)を返すオブジェクト
- `allow(key: str) -> bool` — キー(例: ユーザーID)ごとに、直近 `window_seconds` 秒間のリクエスト数が `max_requests` 未満なら True を返してカウントし、達していれば False を返す(スライディングウィンドウ方式)
- 拒否されたリクエスト(False を返したもの)はカウントに含めない
- ウィンドウは「現在時刻より前の window_seconds 秒間」。ちょうど window_seconds 前の記録はウィンドウに**含まれない**(now - timestamp < window_seconds のものだけ数える)
- キーごとに独立して制限する
- 古い記録はウィンドウ外に出たら消えること(メモリが無限に増えない)

`clock_stub.py` にテスト用の `StubClock`(`now()` と `advance(seconds)`)を用意してあるので使ってください。

実装が仕様どおり動くことを確認してから完了報告してください。
