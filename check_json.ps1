# =============================================
# 1. 検証用 Python コードを一時ファイルに保存
# =============================================
$pythonCode = @'
import json, pathlib, sys

path = pathlib.Path(sys.argv[1])

# エンコーディングを推測して読み込む
raw = path.read_bytes()
try:
    text = raw.decode("utf-8-sig")   # UTF-8 + BOM も許容
except UnicodeDecodeError:
    import chardet
    text = raw.decode(chardet.detect(raw)["encoding"] or "utf-8", errors="replace")

text = text.strip()     # 前後の改行・空白を除去

try:
    json.loads(text)    # 全文が valid JSON なら OK
    print("OK")
except Exception:
    print("NG")
'@

$tmpScript = "$env:TEMP\validate_json_strict.py"
Set-Content -Path $tmpScript -Value $pythonCode -Encoding UTF8

# =============================================
# 2. 判定ループ
# =============================================
$results = @()

foreach ($file in Get-ChildItem out\few_*.txt) {
    $ok = python $tmpScript $file.FullName
    $results += [pscustomobject]@{ File = $file.Name; FewShot = "Yes"; JSON_OK = $ok.Trim() }
}

foreach ($file in Get-ChildItem out\nofew_*.txt) {
    $ok = python $tmpScript $file.FullName
    $results += [pscustomobject]@{ File = $file.Name; FewShot = "No"; JSON_OK = $ok.Trim() }
}

# =============================================
# 3. 結果表示
# =============================================
$results | Format-Table

Write-Host "`n集計:"
$results | Group-Object FewShot, JSON_OK | Format-Table Name, Count

# =============================================
# 4. 後始末
# =============================================
Remove-Item $tmpScript
