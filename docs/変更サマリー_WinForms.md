# DROID Desktop GUI - 変更サマリー

## 実装された変更

### 1. GUIフレームワークの変更

#### 変更前: Tkinter (Python)
```python
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
```
- Python 3.8以上が必要
- クロスプラットフォーム対応
- 外部依存: Python + tkinter

#### 変更後: Windows Forms (PowerShell)
```powershell
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
```
- Windows標準搭載
- 追加インストール不要
- Windows専用

### 2. 新機能: AGENTS.mdファイル指定

#### GUI画面に追加
```
AGENTS.mdファイル:   [                           ] [参照]
```

#### prompt.jsonフォーマット拡張
```json
{
  "prompt": "プロンプト内容",
  "options": {
    "working_directory": ".",
    "model": "claude-sonnet-4-20250514",
    "auto_level": "medium",
    "log_directory": "logs",
    "agents_file": "C:/path/to/AGENTS.md"  // ← 新規追加
  }
}
```

### 3. ファイル構成の変更

#### 追加されたファイル
- `gui_droid_winforms.ps1` - Windows Forms GUI本体
- `docs/GUI使用方法_WinForms.md` - Windows Forms版使用方法
- `docs/GUI画面イメージ_WinForms.md` - 画面レイアウト

#### 変更されたファイル
- `run-droid.bat` - PowerShell GUIを起動するように変更
- `README.md` - Windows Forms版を推奨として更新

#### 残存するファイル（レガシー）
- `gui_droid.py` - Python版GUI（手動起動可能）
- `Test/` - Python版GUI用のテストスイート

## 機能比較表

| 機能 | Windows Forms版 | Python/Tkinter版 |
|------|-----------------|------------------|
| **インストール要件** | なし（Windows標準） | Python 3.8+ |
| **プロンプト入力** | ✅ | ✅ |
| **作業ディレクトリ選択** | ✅ | ✅ |
| **モデル選択** | ✅ (4種類) | ✅ (4種類) |
| **自動化レベル** | ✅ (3段階) | ✅ (3段階) |
| **ログディレクトリ** | ✅ | ✅ |
| **AGENTS.mdファイル** | ✅ **新機能** | ❌ |
| **参照ファイル/フォルダ** | ✅ | ✅ |
| **設定の保存/読み込み** | ✅ | ✅ |
| **DROID実行** | ✅ | ✅ |
| **ステータス表示** | ✅ | ✅ |
| **起動速度** | 速い | やや遅い |
| **UI見た目** | ネイティブWindows | 汎用的 |
| **プラットフォーム** | Windows専用 | クロスプラットフォーム |

## 後方互換性

### ✅ 完全に維持
- 既存の `prompt.json` フォーマットは完全互換
- `agents_file` フィールドは**オプション**（なくても動作）
- 既存の `invoke-droid.ps1` はそのまま使用

### 例: 既存のprompt.json
```json
{
  "prompt": "コードをレビュー",
  "options": {
    "working_directory": ".",
    "model": "claude-sonnet-4-20250514",
    "auto_level": "high",
    "log_directory": "logs",
    "ref_filepath": [
      "./sample/input_data.xlsx"
    ]
  }
}
```
↑ このまま動作します（agents_fileなし）

### 例: AGENTS.mdを使用する場合
```json
{
  "prompt": "カスタムエージェントでレビュー",
  "options": {
    "working_directory": ".",
    "model": "claude-sonnet-4-20250514",
    "auto_level": "high",
    "log_directory": "logs",
    "agents_file": "C:/projects/AGENTS.md",
    "ref_filepath": [
      "./sample/input_data.xlsx"
    ]
  }
}
```

## 利点

### Windows Forms版の利点
1. **追加インストール不要** - Windows標準搭載
2. **ネイティブUI** - Windowsの標準的な見た目と操作性
3. **AGENTS.md対応** - カスタムエージェント設定が可能
4. **高速起動** - Python起動のオーバーヘッドなし
5. **メンテナンス性** - PowerShellのみで完結

### 残されたPython版の利点
1. **クロスプラットフォーム** - Linux/Macでも動作可能
2. **既存のテストスイート** - 25個のテストが利用可能

## 移行ガイド

### ユーザー視点
1. `run-droid.bat` を実行（変更なし）
2. Windows Forms GUIが起動（自動）
3. 使い方は基本的に同じ
4. **新機能**: AGENTS.mdファイル指定が可能に

### 開発者視点
- Python環境のセットアップが不要に
- PowerShellのみでカスタマイズ可能
- `.ps1`ファイルを編集してGUIをカスタマイズ

## テストについて

### Python版のテスト（Test/フォルダ）
- 25個のテストケース
- Python版GUIの機能をテスト
- 引き続き有効（Python版を使用する場合）

### Windows Forms版のテスト
- PowerShellスクリプトの構文は検証済み
- prompt.jsonフォーマットの互換性は維持
- 手動テストで動作確認済み

## 推奨される使用方法

### Windows環境
```
✅ Windows Forms版を使用（推奨）
   - run-droid.bat を実行
   - AGENTS.md機能が必要な場合は必須
```

### Linux/Mac環境
```
⚠️ Python版を手動起動
   - python gui_droid.py を実行
   - AGENTS.md機能は利用不可
```

## まとめ

- ✅ Windows標準のPowerShell Windows Formsに移行完了
- ✅ AGENTS.mdファイル指定機能を追加
- ✅ 既存のprompt.json形式と完全互換
- ✅ Python版はレガシーとして残存
- ✅ ドキュメントを更新・追加

**Windows環境ではWindows Forms版の使用を強く推奨します。**
