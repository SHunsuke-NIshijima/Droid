# Test script to verify Japanese character encoding
# このスクリプトは日本語文字のエンコーディングをテストします

Write-Host "=== DROID GUI エンコーディングテスト ===" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TestFile = Join-Path $ScriptDir "test_japanese_encoding.json"

# テストデータ（日本語文字を含む）
$testData = @{
    prompt = "このコードをレビューして改善点を教えてください。日本語テスト：漢字、ひらがな、カタカナ"
    options = @{
        working_directory = ".\テスト\フォルダ"
        model = "claude-sonnet-4-20250514"
        auto_level = "medium"
        log_directory = "ログ"
        agents_file = "C:\プロジェクト\AGENTS.md"
        ref_filepath = @(
            ".\サンプル\データ.xlsx"
            ".\資料\ドキュメント.txt"
        )
    }
}

Write-Host "1. UTF-8 (BOMなし) で保存テスト..." -ForegroundColor Yellow
try {
    $json = $testData | ConvertTo-Json -Depth 10
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($TestFile, $json, $utf8NoBom)
    Write-Host "   ✓ 保存成功" -ForegroundColor Green
}
catch {
    Write-Host "   ✗ 保存失敗: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. UTF-8で読み込みテスト..." -ForegroundColor Yellow
try {
    $jsonContent = [System.IO.File]::ReadAllText($TestFile, [System.Text.Encoding]::UTF8)
    $loadedData = $jsonContent | ConvertFrom-Json
    Write-Host "   ✓ 読み込み成功" -ForegroundColor Green
}
catch {
    Write-Host "   ✗ 読み込み失敗: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "3. 日本語文字の整合性チェック..." -ForegroundColor Yellow
$errors = @()

if ($loadedData.prompt -ne $testData.prompt) {
    $errors += "プロンプトが一致しません"
}

if ($loadedData.options.working_directory -ne $testData.options.working_directory) {
    $errors += "作業ディレクトリが一致しません"
}

if ($loadedData.options.log_directory -ne $testData.options.log_directory) {
    $errors += "ログディレクトリが一致しません"
}

if ($loadedData.options.agents_file -ne $testData.options.agents_file) {
    $errors += "AGENTS.mdパスが一致しません"
}

if ($errors.Count -eq 0) {
    Write-Host "   ✓ 全ての日本語文字が正しく保存・読み込みされました" -ForegroundColor Green
}
else {
    Write-Host "   ✗ エラーが見つかりました:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "     - $error" -ForegroundColor Red
    }
    exit 1
}

Write-Host ""
Write-Host "4. 保存されたJSONの内容確認..." -ForegroundColor Yellow
Write-Host $jsonContent
Write-Host ""

Write-Host "5. ファイルのBOMチェック..." -ForegroundColor Yellow
$bytes = [System.IO.File]::ReadAllBytes($TestFile)
if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "   ⚠ BOMが検出されました（UTF-8 with BOM）" -ForegroundColor Yellow
}
else {
    Write-Host "   ✓ BOMなし（UTF-8 without BOM）" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== テスト完了 ===" -ForegroundColor Cyan
Write-Host "全てのテストが成功しました！" -ForegroundColor Green
Write-Host ""

# テストファイルをクリーンアップ
Remove-Item $TestFile -ErrorAction SilentlyContinue

exit 0
