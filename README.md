# fable-skills

Fable 5 の作業の進め方(着手前の要件確認、複数角度の調査、実際に動かして検証、結論から報告)を Claude Code の Skill にしたものです。Opus や Sonnet に同じ進め方をさせることで、モデルを変えても作業品質を落とさないようにします。

モデルの推論力そのものは変わりません。変わるのは進め方です。「検証せずに完了と言う」「結論が埋もれた報告」といった進め方の問題を直すだけで、成果物はかなり Fable に近づきます。

## 導入

導入は2つで1セットです。Skill は関連タスクのときだけ読み込まれる仕組みなので、常に効かせたい規律は CLAUDE.md に書く必要があります。

```bash
git clone https://github.com/ohigashi-tky/fable-skills.git
cd fable-skills

# ① Skill をプロジェクトにコピー
mkdir -p /path/to/project/.claude/skills
cp -r skills/* /path/to/project/.claude/skills/

# ② 常時規律を CLAUDE.md に追記
cat templates/CLAUDE-fable-core.md >> /path/to/project/CLAUDE.md
```

全プロジェクトに効かせたい場合は、コピー先を `~/.claude/skills/` と `~/.claude/CLAUDE.md` に変えるだけです。

導入後、プロジェクトで新しいセッションを開いて「使えるスキルを教えて」と聞き、`fable-mode` などが一覧に出れば成功です。

## 使い方

| 場面 | やること |
|---|---|
| 普段のタスク | 何もしない(自動で効く) |
| 品質最優先のタスク | 依頼の先頭に `/fable-mode` を付ける |
| 特定の規律だけ使う | `/adversarial-verify さっきの調査結果を検証して` のように個別に呼ぶ |

## 中身

| Skill | 内容 |
|---|---|
| fable-mode | 全体パイプライン(スコープ確定→調査→実装→検証→報告)。重要タスクの入口 |
| scope-and-plan | 着手前に完了条件と非目標を確定する |
| parallel-explore | 名前・内容・構造・git履歴の複数角度でコードを探す |
| deep-investigate | 調査・分析の多角化と、事実/推論/推測の書き分け |
| adversarial-verify | 結論を報告前に自分で反証してみる |
| evidence-verify | テスト通過で終わらせず、実際に動かして確認する |
| root-cause-debug | 再現→仮説→証拠で絞る→症状でなく原因を直す |
| autonomous-drive | エラーや不足情報で止まらず自力で完遂する |
| context-discipline | 必要な部分だけ読む。長期タスクは状態ノートで管理 |
| quality-pass | 完了前に diff をセルフレビューして削る |
| report-tldr | 結論から書く。確認済みと未確認を分ける |
| plain-writing | README・設計書・コメントを冗長にしない |

## 効果測定

Skills あり/なしをスコアで比較できるベンチマークを同梱しています。使い方は [benchmark/README.md](benchmark/README.md) へ。

## うまく動かないとき

- スキル一覧に出ない → `.claude/skills/fable-mode/SKILL.md` という階層になっているか確認(1階層ズレが定番)
- 規律が効いていない → CLAUDE.md への追記(②)を忘れていないか。`grep "Fable Core" CLAUDE.md` で確認
- 導入したのに反映されない → 既存セッションには反映されない。新しいセッションで試す
