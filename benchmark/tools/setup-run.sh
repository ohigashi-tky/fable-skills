#!/usr/bin/env bash
# ベンチマーク1ラン分の実行環境を作る。
#
# 使い方:
#   ./benchmark/tools/setup-run.sh <T1|T2|T3|T4> <dest-dir> [--with-skills]
#
#   --with-skills: 条件A用。fable-skills の Skill 群と CLAUDE.md 常時規律を実行環境に導入する。
#
# answer-keys/ は絶対にコピーしない(汚染防止)。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

TASK="${1:?タスクID (T1..T4) を指定してください}"
DEST="${2:?コピー先ディレクトリを指定してください}"
WITH_SKILLS="${3:-}"

TASK_DIR=$(ls -d "$REPO_ROOT"/benchmark/tasks/${TASK}-*/ 2>/dev/null | head -1)
if [ -z "$TASK_DIR" ]; then
  echo "エラー: タスク $TASK が見つかりません" >&2
  exit 1
fi

if [ -e "$DEST" ]; then
  echo "エラー: $DEST は既に存在します。ランごとに新しいディレクトリを使ってください(使い回し禁止)" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -r "$TASK_DIR"fixture/. "$DEST"/

if [ "$WITH_SKILLS" = "--with-skills" ]; then
  mkdir -p "$DEST/.claude/skills"
  cp -r "$REPO_ROOT"/skills/* "$DEST/.claude/skills/"
  cat "$REPO_ROOT"/templates/CLAUDE-fable-core.md >> "$DEST/CLAUDE.md"
  CONDITION_HINT="A (Skills あり)"
else
  CONDITION_HINT="B または C (Skills なし)"
fi

# 各ランを独立した git リポジトリにする(diff 確認・状態リセットのため)
git -C "$DEST" init -q
git -C "$DEST" add -A
git -C "$DEST" commit -qm "benchmark fixture: $TASK"

cat <<EOF
実行環境を作成しました: $DEST
  タスク   : $TASK
  条件     : $CONDITION_HINT

次の手順:
  1. Claude Code のモデルを条件に合わせて切り替える (/model)
  2. cd $DEST で新しいセッションを開始する
  3. TASK.md の本文をそのままコピペして依頼する(追加の指示・ヒント禁止)
  4. 完了したら最終報告を $DEST/REPORT.md に保存する
  5. benchmark/answer-keys/$TASK.md の手順で採点し results.csv に追記する
EOF
