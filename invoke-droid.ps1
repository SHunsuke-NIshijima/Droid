# Factory.ai DROID呼び出しスクリプト
# 文字エンコーディング設定
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# prompt.jsonのパス
$PromptFile = Join-Path $ScriptDir "prompt.json"

# prompt.jsonが存在するか確認
if (-not (Test-Path $PromptFile)) {
    Write-Error "prompt.json が見つかりません: $PromptFile"
    exit 1
}

# JSONファイルを読み込み
$PromptData = Get-Content -Path $PromptFile -Raw -Encoding UTF8 | ConvertFrom-Json

# プロンプトを取得
$Prompt = $PromptData.prompt

if ([string]::IsNullOrWhiteSpace($Prompt)) {
    Write-Error "プロンプトが空です。prompt.jsonにプロンプトを入力してください。"
    exit 1
}

Write-Host "=== DROID呼び出し ===" -ForegroundColor Cyan
Write-Host "プロンプト: $Prompt" -ForegroundColor Yellow
Write-Host ""

# 作業ディレクトリの設定
$WorkDir = $ScriptDir
if ($PromptData.options -and $PromptData.options.working_directory) {
    $WorkDir = $PromptData.options.working_directory
    if (-not [System.IO.Path]::IsPathRooted($WorkDir)) {
        $WorkDir = Join-Path $ScriptDir $WorkDir
    }
}

# ログディレクトリの設定
$LogDir = Join-Path $ScriptDir "logs"
if ($PromptData.options.log_directory) {
    $LogDir = $PromptData.options.log_directory
    if (-not [System.IO.Path]::IsPathRooted($LogDir)) {
        $LogDir = Join-Path $ScriptDir $LogDir
    }
}

# ログディレクトリが存在しない場合は作成
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# ログファイル名の生成（タイムスタンプ付き）
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "droid_$Timestamp.log"

Write-Host "ログファイル: $LogFile" -ForegroundColor Gray

# コマンド引数を構築（droid exec用）
$DroidArgs = @()

# モデルの指定
if (-not [string]::IsNullOrWhiteSpace($PromptData.options.model)) {
    $DroidArgs += "--model"
    $DroidArgs += $PromptData.options.model
}

# 自動化レベルの指定（low, medium, high）
if (-not [string]::IsNullOrWhiteSpace($PromptData.options.auto_level)) {
    $DroidArgs += "--auto"
    $DroidArgs += $PromptData.options.auto_level
}

# リアルタイム進捗表示のためstream-json形式を使用
$DroidArgs += "--output-format"
$DroidArgs += "stream-json"

# 作業ディレクトリの指定
$DroidArgs += "--cwd"
$DroidArgs += "`"$WorkDir`""

# プロンプトを追加
$DroidArgs += "`"$Prompt`""

# コマンド文字列を構築（droid execを使用）
$DroidCommand = "droid exec " + ($DroidArgs -join " ")

Write-Host "実行コマンド: $DroidCommand" -ForegroundColor Gray
Write-Host ""

# ログヘッダーを書き込み
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$LogHeader = "================================================================================"
$LogHeader += "`r`nDROID 実行ログ"
$LogHeader += "`r`n================================================================================"
$LogHeader += "`r`n実行日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$LogHeader += "`r`nプロンプト: $Prompt"
$LogHeader += "`r`n作業ディレクトリ: $WorkDir"
$LogHeader += "`r`nモデル: $($PromptData.options.model)"
$LogHeader += "`r`n================================================================================`r`n"
[System.IO.File]::WriteAllText($LogFile, $LogHeader, $utf8NoBom)

# DROIDを呼び出し
try {
    Push-Location $WorkDir
    
    # UTF-8エンコーディング（BOMなし）でStreamWriterを作成
    $logStream = $null
    try {
        $logStream = [System.IO.StreamWriter]::new($LogFile, $true, $utf8NoBom)
        
        # 出力をストリーミング処理しながらコンソールとログファイルに書き込み
        Invoke-Expression $DroidCommand 2>&1 | ForEach-Object {
            $line = $_.ToString()
            Write-Host $line
            # Windows標準のCRLFで統一
            $logStream.Write($line + "`r`n")
        }
    }
    finally {
        # StreamWriterを確実に破棄（null チェック）
        if ($null -ne $logStream) {
            $logStream.Dispose()
        }
    }
    
    $LogFooter = "`r`n================================================================================"
    $LogFooter += "`r`n実行完了: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    $LogFooter += "`r`n================================================================================"
    [System.IO.File]::AppendAllText($LogFile, $LogFooter, $utf8NoBom)
    
    Write-Host ""
    Write-Host "=== 実行完了 ===" -ForegroundColor Green
    Write-Host "ログ保存先: $LogFile" -ForegroundColor Cyan
}
catch {
    $ErrorMsg = "DROIDの呼び出しに失敗しました: $_"
    Write-Error $ErrorMsg
    [System.IO.File]::AppendAllText($LogFile, "ERROR: $ErrorMsg`r`n", $utf8NoBom)
    exit 1
}
finally {
    Pop-Location
}
