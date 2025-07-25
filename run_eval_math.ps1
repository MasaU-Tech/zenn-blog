<#  run_eval_math.ps1
    --------------------------------------------
    math.csv を読み取り、CoT / NoCoT の計算正答率を比較。
    • BOM 付き / なし UTF-8 どちらの CSV でも読める
    • 子プロセスは現在の venv の python を使用
    • 出力に「答え: <数字>円」が無い場合 or RegEx ヒットなし＝NG
#>

# ── 1. 評価ロジックを一時 Python ファイルに書き出し ──
$pythonCode = @'
import csv, re, subprocess, sys, os, pathlib

PY = sys.executable  # 現在の Python (venv) を子プロセスに使う

def run(model_script, question):
    try:
        out = subprocess.check_output(
            [PY, model_script, question],
            text=True, encoding="utf-8", errors="replace"
        )
        # 例: 「答え: 1,900円」, 「答え：１９００円」
        m = re.search(r"答え[:：]?\s*([0-9,０-９]+)", out)
        if not m:
            return None
        num_txt = (
            m.group(1)
             .translate(str.maketrans("０１２３４５６７８９", "0123456789"))
             .replace(",", "")
        )
        return int(num_txt)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"[ERR] {model_script}: {e}\n")
        return None

rows = list(csv.DictReader(open("math.csv", encoding="utf-8-sig")))
for row in rows:
    row["CoT"]   = run("sessions/s11/cot_math.py",    row["Q"])
    row["NoCoT"] = run("sessions/s11/no_cot_math.py", row["Q"])

print(f"{'Question':<35} {'GT':>6} {'CoT':>6} {'No':>6}")
for r in rows:
    print(f"{r['Q'][:30]:<35} {r['A']:>6} {str(r['CoT']):>6} {str(r['NoCoT']):>6}")

cot_ok   = sum(r["CoT"]   == int(r["A"]) for r in rows)
nocot_ok = sum(r["NoCoT"] == int(r["A"]) for r in rows)
print(f"\\n✔︎ 正答   CoT={cot_ok}/{len(rows)} | NoCoT={nocot_ok}/{len(rows)}")
'@

$tmp = "$env:TEMP\\eval_cot.py"
Set-Content -Path $tmp -Value $pythonCode -Encoding UTF8

# ── 2. 実行 ──
python $tmp

# ── 3. 後片付け ──
Remove-Item $tmp