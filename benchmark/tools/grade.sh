#!/usr/bin/env bash
# ベンチマーク1ランを機械採点する。正解を知らない実行役セッションとは別に、採点役が実行する。
#
# 使い方:
#   ./benchmark/tools/grade.sh <T1|T2|T3|T4> <run-dir>
#
# 出力: JSON(auto スコア 0〜100 と内訳)。正解キー・隠しテストは answer-keys/ にあり
# setup-run.sh は実行役の run-dir にそれをコピーしないため、実行役は正解を見られない。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TASK="${1:?タスクID (T1..T4)}"
RUN_DIR="${2:?run ディレクトリ}"

python3 - "$TASK" "$RUN_DIR" <<PY
import sys, json
sys.path.insert(0, "$REPO_ROOT/benchmark/answer-keys")
from grade_lib import GRADERS
task, run_dir = sys.argv[1], sys.argv[2]
result = GRADERS[task](run_dir)
print(json.dumps(result, ensure_ascii=False, indent=2))
PY
