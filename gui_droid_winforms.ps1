# DROID Desktop GUI (PowerShell Windows Forms版)
# Windows標準のWindows Formsを使用したGUIアプリケーション

# 文字エンコーディング設定（日本語対応）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PromptFile = Join-Path $ScriptDir "prompt.json"
$PSScript = Join-Path $ScriptDir "invoke-droid.ps1"

# フォームの作成
$form = New-Object System.Windows.Forms.Form
$form.Text = "DROID Desktop GUI"
$form.Size = New-Object System.Drawing.Size(850, 810)
$form.StartPosition = "CenterScreen"
$form.MinimumSize = New-Object System.Drawing.Size(850, 810)

# フォントの設定
$defaultFont = New-Object System.Drawing.Font("MS UI Gothic", 9)

# Y位置のトラッキング
$yPos = 10

# === プロンプト入力エリア ===
$lblPrompt = New-Object System.Windows.Forms.Label
$lblPrompt.Location = New-Object System.Drawing.Point(10, $yPos)
$lblPrompt.Size = New-Object System.Drawing.Size(800, 20)
$lblPrompt.Text = "プロンプト (Prompt) *"
$lblPrompt.Font = $defaultFont
$form.Controls.Add($lblPrompt)

$yPos += 25

$txtPrompt = New-Object System.Windows.Forms.TextBox
$txtPrompt.Location = New-Object System.Drawing.Point(10, $yPos)
$txtPrompt.Size = New-Object System.Drawing.Size(810, 120)
$txtPrompt.Multiline = $true
$txtPrompt.ScrollBars = "Vertical"
$txtPrompt.Font = $defaultFont
$form.Controls.Add($txtPrompt)

$yPos += 130

# === オプション設定グループ ===
$grpOptions = New-Object System.Windows.Forms.GroupBox
$grpOptions.Location = New-Object System.Drawing.Point(10, $yPos)
$grpOptions.Size = New-Object System.Drawing.Size(810, 230)
$grpOptions.Text = "オプション設定"
$grpOptions.Font = $defaultFont
$form.Controls.Add($grpOptions)

# 作業ディレクトリ
$lblWorkDir = New-Object System.Windows.Forms.Label
$lblWorkDir.Location = New-Object System.Drawing.Point(10, 25)
$lblWorkDir.Size = New-Object System.Drawing.Size(120, 20)
$lblWorkDir.Text = "作業ディレクトリ:"
$lblWorkDir.Font = $defaultFont
$grpOptions.Controls.Add($lblWorkDir)

$txtWorkDir = New-Object System.Windows.Forms.TextBox
$txtWorkDir.Location = New-Object System.Drawing.Point(140, 23)
$txtWorkDir.Size = New-Object System.Drawing.Size(550, 20)
$txtWorkDir.Text = "."
$txtWorkDir.Font = $defaultFont
$grpOptions.Controls.Add($txtWorkDir)

$btnBrowseWorkDir = New-Object System.Windows.Forms.Button
$btnBrowseWorkDir.Location = New-Object System.Drawing.Point(700, 22)
$btnBrowseWorkDir.Size = New-Object System.Drawing.Size(80, 23)
$btnBrowseWorkDir.Text = "参照"
$btnBrowseWorkDir.Font = $defaultFont
$grpOptions.Controls.Add($btnBrowseWorkDir)

# モデル選択
$lblModel = New-Object System.Windows.Forms.Label
$lblModel.Location = New-Object System.Drawing.Point(10, 55)
$lblModel.Size = New-Object System.Drawing.Size(120, 20)
$lblModel.Text = "モデル:"
$lblModel.Font = $defaultFont
$grpOptions.Controls.Add($lblModel)

$cmbModel = New-Object System.Windows.Forms.ComboBox
$cmbModel.Location = New-Object System.Drawing.Point(140, 53)
$cmbModel.Size = New-Object System.Drawing.Size(550, 20)
$cmbModel.DropDownStyle = "DropDownList"
$cmbModel.Font = $defaultFont
$cmbModel.Items.AddRange(@(
    "claude-opus-4-5-20251101",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20241022",
    "claude-haiku-4-20250116"
))
$cmbModel.SelectedIndex = 1
$grpOptions.Controls.Add($cmbModel)

# 自動化レベル
$lblAutoLevel = New-Object System.Windows.Forms.Label
$lblAutoLevel.Location = New-Object System.Drawing.Point(10, 85)
$lblAutoLevel.Size = New-Object System.Drawing.Size(120, 20)
$lblAutoLevel.Text = "自動化レベル:"
$lblAutoLevel.Font = $defaultFont
$grpOptions.Controls.Add($lblAutoLevel)

$cmbAutoLevel = New-Object System.Windows.Forms.ComboBox
$cmbAutoLevel.Location = New-Object System.Drawing.Point(140, 83)
$cmbAutoLevel.Size = New-Object System.Drawing.Size(550, 20)
$cmbAutoLevel.DropDownStyle = "DropDownList"
$cmbAutoLevel.Font = $defaultFont
$cmbAutoLevel.Items.AddRange(@("low", "medium", "high"))
$cmbAutoLevel.SelectedIndex = 1
$grpOptions.Controls.Add($cmbAutoLevel)

# ログディレクトリ
$lblLogDir = New-Object System.Windows.Forms.Label
$lblLogDir.Location = New-Object System.Drawing.Point(10, 115)
$lblLogDir.Size = New-Object System.Drawing.Size(120, 20)
$lblLogDir.Text = "ログディレクトリ:"
$lblLogDir.Font = $defaultFont
$grpOptions.Controls.Add($lblLogDir)

$txtLogDir = New-Object System.Windows.Forms.TextBox
$txtLogDir.Location = New-Object System.Drawing.Point(140, 113)
$txtLogDir.Size = New-Object System.Drawing.Size(550, 20)
$txtLogDir.Text = "logs"
$txtLogDir.Font = $defaultFont
$grpOptions.Controls.Add($txtLogDir)

$btnBrowseLogDir = New-Object System.Windows.Forms.Button
$btnBrowseLogDir.Location = New-Object System.Drawing.Point(700, 112)
$btnBrowseLogDir.Size = New-Object System.Drawing.Size(80, 23)
$btnBrowseLogDir.Text = "参照"
$btnBrowseLogDir.Font = $defaultFont
$grpOptions.Controls.Add($btnBrowseLogDir)

# AGENTS.mdファイル (新規追加)
$lblAgentsFile = New-Object System.Windows.Forms.Label
$lblAgentsFile.Location = New-Object System.Drawing.Point(10, 145)
$lblAgentsFile.Size = New-Object System.Drawing.Size(120, 20)
$lblAgentsFile.Text = "AGENTS.mdファイル:"
$lblAgentsFile.Font = $defaultFont
$grpOptions.Controls.Add($lblAgentsFile)

$txtAgentsFile = New-Object System.Windows.Forms.TextBox
$txtAgentsFile.Location = New-Object System.Drawing.Point(140, 143)
$txtAgentsFile.Size = New-Object System.Drawing.Size(550, 20)
$txtAgentsFile.Text = ""
$txtAgentsFile.Font = $defaultFont
$grpOptions.Controls.Add($txtAgentsFile)

$btnBrowseAgentsFile = New-Object System.Windows.Forms.Button
$btnBrowseAgentsFile.Location = New-Object System.Drawing.Point(700, 142)
$btnBrowseAgentsFile.Size = New-Object System.Drawing.Size(80, 23)
$btnBrowseAgentsFile.Text = "参照"
$btnBrowseAgentsFile.Font = $defaultFont
$grpOptions.Controls.Add($btnBrowseAgentsFile)

# MCPサーバー
$lblMcpServer = New-Object System.Windows.Forms.Label
$lblMcpServer.Location = New-Object System.Drawing.Point(10, 175)
$lblMcpServer.Size = New-Object System.Drawing.Size(120, 20)
$lblMcpServer.Text = "MCPサーバー:"
$lblMcpServer.Font = $defaultFont
$grpOptions.Controls.Add($lblMcpServer)

$txtMcpServer = New-Object System.Windows.Forms.TextBox
$txtMcpServer.Location = New-Object System.Drawing.Point(140, 173)
$txtMcpServer.Size = New-Object System.Drawing.Size(640, 20)
$txtMcpServer.Text = ""
$txtMcpServer.Font = $defaultFont
$txtMcpServer.PlaceholderText = "例: npx @anthropic/mcp-server-filesystem"
$grpOptions.Controls.Add($txtMcpServer)

$yPos += 240

# === 参照ファイル/フォルダグループ ===
$grpRef = New-Object System.Windows.Forms.GroupBox
$grpRef.Location = New-Object System.Drawing.Point(10, $yPos)
$grpRef.Size = New-Object System.Drawing.Size(810, 180)
$grpRef.Text = "参照ファイル/フォルダ"
$grpRef.Font = $defaultFont
$form.Controls.Add($grpRef)

$lstRef = New-Object System.Windows.Forms.ListBox
$lstRef.Location = New-Object System.Drawing.Point(10, 25)
$lstRef.Size = New-Object System.Drawing.Size(680, 140)
$lstRef.Font = $defaultFont
$grpRef.Controls.Add($lstRef)

$btnAddFile = New-Object System.Windows.Forms.Button
$btnAddFile.Location = New-Object System.Drawing.Point(700, 25)
$btnAddFile.Size = New-Object System.Drawing.Size(90, 30)
$btnAddFile.Text = "ファイル追加"
$btnAddFile.Font = $defaultFont
$grpRef.Controls.Add($btnAddFile)

$btnAddFolder = New-Object System.Windows.Forms.Button
$btnAddFolder.Location = New-Object System.Drawing.Point(700, 60)
$btnAddFolder.Size = New-Object System.Drawing.Size(90, 30)
$btnAddFolder.Text = "フォルダ追加"
$btnAddFolder.Font = $defaultFont
$grpRef.Controls.Add($btnAddFolder)

$btnRemove = New-Object System.Windows.Forms.Button
$btnRemove.Location = New-Object System.Drawing.Point(700, 95)
$btnRemove.Size = New-Object System.Drawing.Size(90, 30)
$btnRemove.Text = "削除"
$btnRemove.Font = $defaultFont
$grpRef.Controls.Add($btnRemove)

$yPos += 190

# === ステータス表示エリア ===
$grpStatus = New-Object System.Windows.Forms.GroupBox
$grpStatus.Location = New-Object System.Drawing.Point(10, $yPos)
$grpStatus.Size = New-Object System.Drawing.Size(810, 150)
$grpStatus.Text = "実行進捗・ステータス"
$grpStatus.Font = $defaultFont
$form.Controls.Add($grpStatus)

$txtStatus = New-Object System.Windows.Forms.TextBox
$txtStatus.Location = New-Object System.Drawing.Point(10, 20)
$txtStatus.Size = New-Object System.Drawing.Size(785, 120)
$txtStatus.Multiline = $true
$txtStatus.ScrollBars = "Vertical"
$txtStatus.ReadOnly = $true
$txtStatus.Font = $defaultFont
$txtStatus.Text = "待機中"
$grpStatus.Controls.Add($txtStatus)

$yPos += 160

# === ボタンエリア ===
$btnReload = New-Object System.Windows.Forms.Button
$btnReload.Location = New-Object System.Drawing.Point(550, $yPos)
$btnReload.Size = New-Object System.Drawing.Size(80, 30)
$btnReload.Text = "読み込み"
$btnReload.Font = $defaultFont
$form.Controls.Add($btnReload)

$btnSave = New-Object System.Windows.Forms.Button
$btnSave.Location = New-Object System.Drawing.Point(640, $yPos)
$btnSave.Size = New-Object System.Drawing.Size(80, 30)
$btnSave.Text = "保存"
$btnSave.Font = $defaultFont
$form.Controls.Add($btnSave)

$btnExecute = New-Object System.Windows.Forms.Button
$btnExecute.Location = New-Object System.Drawing.Point(730, $yPos)
$btnExecute.Size = New-Object System.Drawing.Size(90, 30)
$btnExecute.Text = "実行"
$btnExecute.Font = New-Object System.Drawing.Font("MS UI Gothic", 9, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($btnExecute)

# === イベントハンドラー ===

# 作業ディレクトリ参照
$btnBrowseWorkDir.Add_Click({
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "作業ディレクトリを選択"
    $folderBrowser.SelectedPath = $ScriptDir
    if ($folderBrowser.ShowDialog() -eq "OK") {
        $txtWorkDir.Text = $folderBrowser.SelectedPath
    }
})

# ログディレクトリ参照
$btnBrowseLogDir.Add_Click({
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "ログディレクトリを選択"
    $folderBrowser.SelectedPath = $ScriptDir
    if ($folderBrowser.ShowDialog() -eq "OK") {
        $txtLogDir.Text = $folderBrowser.SelectedPath
    }
})

# AGENTS.mdファイル参照
$btnBrowseAgentsFile.Add_Click({
    $fileBrowser = New-Object System.Windows.Forms.OpenFileDialog
    $fileBrowser.Filter = "Markdown Files (*.md)|*.md|All Files (*.*)|*.*"
    $fileBrowser.Title = "AGENTS.mdファイルを選択"
    $fileBrowser.InitialDirectory = $ScriptDir
    if ($fileBrowser.ShowDialog() -eq "OK") {
        $txtAgentsFile.Text = $fileBrowser.FileName
    }
})

# ファイル追加
$btnAddFile.Add_Click({
    $fileBrowser = New-Object System.Windows.Forms.OpenFileDialog
    $fileBrowser.Multiselect = $true
    $fileBrowser.Title = "参照ファイルを選択"
    $fileBrowser.InitialDirectory = $ScriptDir
    if ($fileBrowser.ShowDialog() -eq "OK") {
        foreach ($file in $fileBrowser.FileNames) {
            $lstRef.Items.Add($file)
        }
    }
})

# フォルダ追加
$btnAddFolder.Add_Click({
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "参照フォルダを選択"
    $folderBrowser.SelectedPath = $ScriptDir
    if ($folderBrowser.ShowDialog() -eq "OK") {
        $lstRef.Items.Add($folderBrowser.SelectedPath)
    }
})

# 削除
$btnRemove.Add_Click({
    if ($lstRef.SelectedIndex -ge 0) {
        $lstRef.Items.RemoveAt($lstRef.SelectedIndex)
    }
})

# 設定を読み込み
function Load-Settings {
    if (Test-Path $PromptFile) {
        try {
            # UTF-8エンコーディングで読み込み（BOM有無に対応）
            $jsonContent = [System.IO.File]::ReadAllText($PromptFile, [System.Text.Encoding]::UTF8)
            $data = $jsonContent | ConvertFrom-Json
            
            $txtPrompt.Text = $data.prompt
            
            if ($data.options) {
                if ($data.options.working_directory) {
                    $txtWorkDir.Text = $data.options.working_directory
                }
                if ($data.options.model) {
                    $index = $cmbModel.Items.IndexOf($data.options.model)
                    if ($index -ge 0) {
                        $cmbModel.SelectedIndex = $index
                    }
                }
                if ($data.options.auto_level) {
                    $index = $cmbAutoLevel.Items.IndexOf($data.options.auto_level)
                    if ($index -ge 0) {
                        $cmbAutoLevel.SelectedIndex = $index
                    }
                }
                if ($data.options.log_directory) {
                    $txtLogDir.Text = $data.options.log_directory
                }
                if ($data.options.agents_file) {
                    $txtAgentsFile.Text = $data.options.agents_file
                }
                if ($data.options.mcp_server) {
                    $txtMcpServer.Text = $data.options.mcp_server
                }
                if ($data.options.ref_filepath) {
                    $lstRef.Items.Clear()
                    foreach ($path in $data.options.ref_filepath) {
                        $lstRef.Items.Add($path)
                    }
                }
            }
            
            $txtStatus.Text = "設定を読み込みました。"
        }
        catch {
            $txtStatus.Text = "設定の読み込みに失敗しました: $($_.Exception.Message)"
            [System.Windows.Forms.MessageBox]::Show("設定の読み込みに失敗しました:`r`n$($_.Exception.Message)", "エラー", "OK", "Error")
        }
    }
    else {
        $txtStatus.Text = "prompt.jsonが見つかりません。デフォルト設定を使用します。"
    }
}

# 設定を保存
function Save-Settings {
    if ([string]::IsNullOrWhiteSpace($txtPrompt.Text)) {
        [System.Windows.Forms.MessageBox]::Show("プロンプトを入力してください。", "警告", "OK", "Warning")
        return $false
    }
    
    $refPaths = @()
    foreach ($item in $lstRef.Items) {
        $refPaths += $item.ToString()
    }
    
    $data = @{
        prompt = $txtPrompt.Text
        options = @{
            working_directory = $txtWorkDir.Text
            model = $cmbModel.SelectedItem.ToString()
            auto_level = $cmbAutoLevel.SelectedItem.ToString()
            log_directory = $txtLogDir.Text
        }
    }
    
    # AGENTS.mdファイルが指定されている場合のみ追加
    if (-not [string]::IsNullOrWhiteSpace($txtAgentsFile.Text)) {
        $data.options.agents_file = $txtAgentsFile.Text
    }
    
    # MCPサーバーが指定されている場合のみ追加
    if (-not [string]::IsNullOrWhiteSpace($txtMcpServer.Text)) {
        $data.options.mcp_server = $txtMcpServer.Text
    }
    
    # 参照パスがある場合のみ追加
    if ($refPaths.Count -gt 0) {
        $data.options.ref_filepath = $refPaths
    }
    
    try {
        $json = $data | ConvertTo-Json -Depth 10
        # UTF-8 without BOMで保存（日本語文字化け対策）
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($PromptFile, $json, $utf8NoBom)
        $txtStatus.Text = "設定を保存しました。"
        return $true
    }
    catch {
        $txtStatus.Text = "設定の保存に失敗しました: $($_.Exception.Message)"
        [System.Windows.Forms.MessageBox]::Show("設定の保存に失敗しました:`r`n$($_.Exception.Message)", "エラー", "OK", "Error")
        return $false
    }
}

# 読み込みボタン
$btnReload.Add_Click({
    Load-Settings
})

# 保存ボタン
$btnSave.Add_Click({
    if (Save-Settings) {
        [System.Windows.Forms.MessageBox]::Show("設定をprompt.jsonに保存しました。", "成功", "OK", "Information")
    }
})

# 実行ボタン
$btnExecute.Add_Click({
    if ([string]::IsNullOrWhiteSpace($txtPrompt.Text)) {
        [System.Windows.Forms.MessageBox]::Show("プロンプトを入力してください。", "警告", "OK", "Warning")
        return
    }
    
    # 設定を保存
    $txtStatus.Text = "設定を保存しています..."
    $form.Refresh()
    
    if (-not (Save-Settings)) {
        return
    }
    
    # PowerShellスクリプトの存在確認
    if (-not (Test-Path $PSScript)) {
        $txtStatus.Text = "エラー: invoke-droid.ps1が見つかりません"
        [System.Windows.Forms.MessageBox]::Show("invoke-droid.ps1が見つかりません: $PSScript", "エラー", "OK", "Error")
        return
    }
    
    # ボタンを無効化
    $btnExecute.Enabled = $false
    $btnSave.Enabled = $false
    $btnReload.Enabled = $false
    
    $txtStatus.Text = "DROIDを実行中...`r`n"
    $form.Refresh()
    
    try {
        # PowerShellスクリプトを実行（出力をリダイレクト）
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "powershell.exe"
        $processInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSScript`""
        $processInfo.WorkingDirectory = $ScriptDir
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $false
        $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        
        # 出力イベントハンドラーを追加（リアルタイム表示）
        $outputHandler = {
            param($sender, $e)
            if (-not [string]::IsNullOrEmpty($e.Data)) {
                $txtStatus.Invoke([Action]{
                    $txtStatus.AppendText($e.Data + "`r`n")
                    $txtStatus.SelectionStart = $txtStatus.Text.Length
                    $txtStatus.ScrollToCaret()
                })
            }
        }
        
        $eventSubscription = Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outputHandler
        
        # プロセスを開始
        $process.Start() | Out-Null
        $process.BeginOutputReadLine()
        
        # プロセスの終了を待つ
        $process.WaitForExit()
        
        # イベントハンドラーをクリーンアップ
        if ($eventSubscription) {
            Unregister-Event -SourceIdentifier $eventSubscription.Name
        }
        
        # エラー出力を取得
        $stderr = $process.StandardError.ReadToEnd()
        
        if ($process.ExitCode -eq 0) {
            $txtStatus.AppendText("`r`n実行完了しました。")
            [System.Windows.Forms.MessageBox]::Show("DROIDの実行が完了しました。", "完了", "OK", "Information")
        }
        else {
            $errorMsg = if ([string]::IsNullOrWhiteSpace($stderr)) { "実行が失敗しました (終了コード: $($process.ExitCode))" } else { $stderr }
            $txtStatus.AppendText("`r`nエラー: $errorMsg")
            [System.Windows.Forms.MessageBox]::Show("DROIDの実行に失敗しました。`r`n$errorMsg", "エラー", "OK", "Error")
        }
    }
    catch {
        $txtStatus.AppendText("`r`n実行エラー: $($_.Exception.Message)")
        [System.Windows.Forms.MessageBox]::Show("実行中にエラーが発生しました:`r`n$($_.Exception.Message)", "エラー", "OK", "Error")
    }
    finally {
        # ボタンを有効化
        $btnExecute.Enabled = $true
        $btnSave.Enabled = $true
        $btnReload.Enabled = $true
    }
})

# 初回起動時に設定を読み込み
Load-Settings

# フォームを表示
[void]$form.ShowDialog()
