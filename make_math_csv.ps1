<#  make_math_csv.ps1
    ───────────────────────────────────────────────────────
    Few-Shot / CoT 検証用の CSV を新規生成するスクリプト
    • 出力先 : このスクリプトと同じフォルダーに math.csv
    • 文字コード : UTF-8 (BOM なし)
#>

$csvContent = @'
Q,A
500円のりんごを3個と200円のバナナを2本買うと合計はいくら？,1900
700円の本を4冊、税10%を加えた総額は？,3080
'@

# 保存先パス
$csvPath = Join-Path $PSScriptRoot "math.csv"

# UTF-8 (BOM なし) で書き込み
[System.IO.File]::WriteAllText(
    $csvPath,
    $csvContent,
    [System.Text.UTF8Encoding]::new($false)   # $false = BOM なし
)

Write-Host "✅ math.csv を生成しました → $csvPath"
