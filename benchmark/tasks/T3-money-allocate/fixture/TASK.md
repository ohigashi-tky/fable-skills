# 依頼

`money.py` に、金額を整数セントで扱う `Money` クラスと、金額を比率で分配する `allocate` 関数を実装してください。テスト用スタブなどはありません。仕様に厳密に従ってください。

## `Money` クラス

- `Money(cents, currency)` で生成する。
- `cents` は**必ず int**。int 以外(float / bool は int のサブクラスだが float は不可)が渡されたら `TypeError`。
- `currency` は**3文字の文字列**(例 `"USD"`)。3文字でない、または str でなければ `ValueError`。
- `add(other)` / `subtract(other)` — 同じ通貨の `Money` を返す。`other` が `Money` でなければ `TypeError`、通貨が違えば `ValueError`。
- 同じ cents・同じ currency の `Money` は等値(`==`)とみなす。

## `allocate(amount_cents, ratios)` 関数

整数セント `amount_cents` を、比率のリスト `ratios` に従って分配し、**整数セントのリスト**を返す。

- 戻り値の合計は `amount_cents` に**厳密に一致**する(1セントも失われない・増えない)。
- 分配は最大剰余方式: 各要素の正確な取り分(有理数)を計算し、まず**負の無限大方向に切り捨て**(floor)、余ったセントを**剰余(取り分の小数部)が大きい要素から1セントずつ**加える。剰余が同じ要素同士は**インデックスの小さい方**を優先する。
- `amount_cents` が負の場合も合計が厳密に一致すること(floor は負の無限大方向)。
- `ratios` の各要素は非負の数(int または float)。負の要素があれば `ValueError`。
- `ratios` は正規化されていなくてよい(合計が1でなくてよい。比率として扱う)。
- `ratios` が空なら `ValueError`。全要素が0なら `ValueError`。
- `amount_cents` が int でなければ `TypeError`。
- 比率が0の要素には0が割り当たる。

### 例

- `allocate(100, [1, 1, 1])` → `[34, 33, 33]`
- `allocate(10, [1, 1, 1])` → `[4, 3, 3]`(余り1はインデックス0へ)
- `allocate(-100, [1, 1, 1])` → `[-33, -33, -34]`(floorで各-34、余り2を剰余最大の先頭2要素へ)
- `allocate(100, [0, 1, 1])` → `[0, 50, 50]`

実装が仕様どおり動くことを確認してから完了報告してください。境界(負の金額・比率0・端数の分配順)まで自分でテストすること。
