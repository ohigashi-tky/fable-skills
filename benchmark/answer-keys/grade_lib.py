"""採点ロジック(スクリプト機械採点)。実行役セッションには渡さない。

各 grade_* は run ディレクトリのパスを受け取り、0〜100 の auto スコアと詳細を返す。
正解を知る人間・LLM を介さず、隠しテスト実行と正解キー照合だけで採点する。
"""

import json
import os
import re
import subprocess
import sys

KEYDIR = os.path.dirname(os.path.abspath(__file__))


def _run_pytest(run_dir, test_src, test_name):
    """test_src を run_dir にコピーして pytest 実行、(passed, total) を返す。"""
    dst = os.path.join(run_dir, test_name)
    with open(test_src) as f:
        open(dst, "w").write(f.read())
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", test_name, "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=run_dir, capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    passed = len(re.findall(r"\bPASSED\b", out))
    if passed == 0:
        m = re.search(r"(\d+) passed", out)
        passed = int(m.group(1)) if m else 0
    failed = 0
    m = re.search(r"(\d+) failed", out)
    if m:
        failed = int(m.group(1))
    errors = 0
    m = re.search(r"(\d+) error", out)
    if m:
        errors = int(m.group(1))
    total = passed + failed + errors
    if total == 0:
        # 収集エラー(import 失敗など)は全滅扱い
        return 0, None, out
    return passed, total, out


def grade_T2(run_dir):
    passed, total, out = _run_pytest(run_dir, os.path.join(KEYDIR, "T2_hidden_test.py"), "_hidden_T2.py")
    if total is None:
        return {"auto": 0.0, "detail": "テスト収集失敗(import不能)", "log": out[-400:]}
    score = round(passed / total * 100, 1)
    return {"auto": score, "detail": f"隠しテスト {passed}/{total} 通過", "passed": passed, "total": total}


def grade_T3(run_dir):
    passed, total, out = _run_pytest(run_dir, os.path.join(KEYDIR, "T3_hidden_test.py"), "_hidden_T3.py")
    if total is None:
        return {"auto": 0.0, "detail": "テスト収集失敗(money.py未実装/import不能)", "log": out[-400:]}
    score = round(passed / total * 100, 1)
    return {"auto": score, "detail": f"受入テスト {passed}/{total} 通過", "passed": passed, "total": total}


def grade_T1(run_dir):
    key = json.load(open(os.path.join(KEYDIR, "T1_bugmap.json")))
    tol = key["line_tolerance"]
    true_lines = [b["line"] for b in key["bugs"]]
    fpath = os.path.join(run_dir, "findings.json")
    if not os.path.exists(fpath):
        return {"auto": 0.0, "detail": "findings.json がない"}
    try:
        found = json.load(open(fpath))
        reported = [int(e["line"]) for e in found]
    except Exception as e:
        return {"auto": 0.0, "detail": f"findings.json 解析失敗: {e}"}
    matched = set()
    fp = 0
    for ln in reported:
        hit = None
        for tl in true_lines:
            if abs(ln - tl) <= tol and tl not in matched:
                hit = tl
                break
        if hit is not None:
            matched.add(hit)
        else:
            # 既にmatched済みの行への重複報告はFPに数えない。真バグ行の近傍でもないものだけFP
            near_any = any(abs(ln - tl) <= tol for tl in true_lines)
            if not near_any:
                fp += 1
    n = key["total_bugs"]
    per = 100.0 / n
    score = max(0.0, len(matched) * per - fp * per)
    return {"auto": round(score, 1),
            "detail": f"発見 {len(matched)}/{n}・誤検出 {fp}",
            "matched": len(matched), "false_positives": fp}


def _norm(s):
    return re.sub(r"\s+", "", str(s)).lower()


def grade_T4(run_dir):
    key = json.load(open(os.path.join(KEYDIR, "T4_answers_key.json")))["questions"]
    fpath = os.path.join(run_dir, "answers.json")
    if not os.path.exists(fpath):
        return {"auto": 0.0, "detail": "answers.json がない"}
    try:
        ans = json.load(open(fpath))
    except Exception as e:
        return {"auto": 0.0, "detail": f"answers.json 解析失敗: {e}"}
    got = 0.0
    perq = {}
    for q, spec in key.items():
        a = _norm(ans.get(q, ""))
        score = 0.0
        if a:
            if "reject_if_contains" in spec and any(_norm(r) in a for r in spec["reject_if_contains"]):
                score = 0.0
            elif any(_norm(x) in a for x in spec["accept"]):
                if "must_also_contain_any" in spec and not any(_norm(x) in a for x in spec["must_also_contain_any"]):
                    score = 0.5
                else:
                    score = 1.0
            elif "partial" in spec and any(_norm(x) in a for x in spec["partial"]):
                score = 0.5
        perq[q] = score
        got += score
    n = len(key)
    return {"auto": round(got / n * 100, 1), "detail": f"正答 {got}/{n}", "perq": perq}


GRADERS = {"T1": grade_T1, "T2": grade_T2, "T3": grade_T3, "T4": grade_T4}
