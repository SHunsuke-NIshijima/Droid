# PowerShellからDROIDを呼び出す

Factory.aiのDROIDをPowerShell経由で呼び出すためのツールです。

## ファイル構成

```
PowerShell/
├── run-droid.bat      # 実行用バッチファイル
├── invoke-droid.ps1   # PowerShellスクリプト
├── prompt.json        # プロンプト設定ファイル
└── README.md          # このファイル
```

## 使い方

### 1. prompt.jsonにプロンプトを記述

```json
{
    "prompt": "ここにDROIDへの指示を書く",
    "options": {
        "working_directory": "."
    }
}
```

### 2. run-droid.batを実行

バッチファイルをダブルクリックするか、コマンドラインから実行します。

```cmd
run-droid.bat
```

## prompt.jsonの設定

| プロパティ | 説明 | 例 |
|-----------|------|-----|
| `prompt` | DROIDへの指示内容 | `"このコードをレビューして"` |
| `options.working_directory` | 作業ディレクトリ（相対パスまたは絶対パス） | `"."` または `"C:/projects/myapp"` |
| `options.reference_paths` | 参照ファイル/フォルダパスの配列 | `["src/main.py", "docs/"]` |
| `options.model` | 使用するAIモデル | `"claude-sonnet-4-20250514"`, `"claude-opus-4-20250514"` |
| `options.auto_level` | 自動承認レベル（low, medium, high） | `"low"`, `"medium"`, `"high"` |
| `options.log_directory` | ログ出力先ディレクトリ | `"logs"` または `"C:/logs/droid"` |

### prompt.jsonの完全な例

```json
{
    "prompt": "このプロジェクトのコードをレビューして改善点を教えて",
    "options": {
        "working_directory": "C:/projects/myapp",
        "reference_paths": [
            "src/main.py",
            "src/utils/",
            "config.json"
        ],
        "model": "claude-sonnet-4-20250514",
        "auto_level": "medium",
        "log_directory": "logs"
    }
}
```

## ログ出力機能

実行するたびに`logs`フォルダ（またはlog_directoryで指定したフォルダ）にログファイルが自動生成されます。

### ログに含まれる内容
- 実行日時
- プロンプト内容
- 作業ディレクトリ
- 使用モデル
- **DROIDの検討過程（思考プロセス）**
- 実行結果
- 完了時刻

### ログファイル名
```
droid_YYYYMMDD_HHMMSS.log
```
例: `droid_20260110_143052.log`

## プロンプトの例

### ファイル操作
```json
{
    "prompt": "このフォルダ内のファイル一覧を表示して",
    "options": { "working_directory": "." }
}
```

### コード作成
```json
{
    "prompt": "Pythonで簡単なTODOリストアプリを作成して",
    "options": { "working_directory": "." }
}
```

### プロジェクト分析
```json
{
    "prompt": "このプロジェクトの構造を説明して",
    "options": { "working_directory": "C:/path/to/your/project" }
}
```

### バグ修正
```json
{
    "prompt": "main.pyのエラーを修正して",
    "options": { "working_directory": "." }
}
```

### リファクタリング
```json
{
    "prompt": "utils.jsのコードを読みやすくリファクタリングして",
    "options": { "working_directory": "." }
}
```

## 前提条件

- Factory.aiのDROIDがインストールされていること
- `droid`コマンドがPATHに通っていること

## トラブルシューティング

### 「droidコマンドが見つからない」エラー
→ DROIDが正しくインストールされているか、PATHが設定されているか確認してください。

### 「prompt.jsonが見つからない」エラー
→ prompt.jsonがinvoke-droid.ps1と同じフォルダにあるか確認してください。

### 文字化けする場合
→ prompt.jsonをUTF-8で保存してください。
