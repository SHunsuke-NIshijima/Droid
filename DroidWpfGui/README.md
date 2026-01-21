# DROID WPF GUI

ModernWpf を使用したモダンなデザインの Windows Presentation Foundation (WPF) GUI です。

## 特徴

- ✅ **モダンなデザイン**: [ModernWpf](https://github.com/Kinnara/ModernWpf) ライブラリを使用した現代的なUI
- ✅ WPF による高度なグラフィカル操作
- ✅ プロンプトとパラメータを直感的に入力
- ✅ ファイル/フォルダの参照が簡単
- ✅ AGENTS.mdファイルの指定が可能
- ✅ 実行状態のリアルタイム表示
- ✅ 実行進捗のリアルタイム表示

## 必須環境

- Windows 10/11
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) 以上
- [Factory.ai DROID](https://www.factory.ai/droid)

## 起動方法

### 方法1: バッチファイルから起動（推奨）

```cmd
run-droid-wpf.bat
```

### 方法2: コマンドラインから起動

```cmd
cd DroidWpfGui
dotnet run
```

### 方法3: ビルドして実行ファイルを作成

```cmd
cd DroidWpfGui
dotnet build -c Release
cd bin\Release\net8.0-windows
DroidWpfGui.exe
```

## プロジェクト構成

```
DroidWpfGui/
├── DroidWpfGui.csproj      # プロジェクトファイル（ModernWpf参照を含む）
├── App.xaml                # アプリケーション定義（ModernWpfテーマ設定）
├── App.xaml.cs             # アプリケーションコード
├── MainWindow.xaml         # メインウィンドウUI（ModernWpfコントロール使用）
└── MainWindow.xaml.cs      # メインウィンドウロジック
```

## ModernWpf について

このGUIは [ModernWpf](https://github.com/Kinnara/ModernWpf) ライブラリを使用しています。

ModernWpf は WPF アプリケーションに Windows 10/11 の Fluent Design System を導入するライブラリで、以下の機能を提供します：

- モダンなコントロールデザイン
- ライト/ダークテーマのサポート
- アクセント カラーのカスタマイズ
- Windows 11 スタイルの UI 要素

## 使用方法

1. **プロンプト入力**: DROIDに実行させたい内容を入力
2. **オプション設定**: 
   - 作業ディレクトリ
   - AIモデル選択
   - 自動化レベル
   - ログ出力先
   - AGENTS.mdファイル（オプション）
3. **参照ファイル/フォルダ**: DROIDに参照させたいファイルやフォルダを追加
4. **実行**: 「実行」ボタンをクリック

設定は自動的に `prompt.json` に保存されます。

## トラブルシューティング

### .NET SDK がインストールされていない

```
Error: .NET SDK is not installed.
```

→ [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) をインストールしてください。

### droidコマンドが見つからない

→ Factory.ai DROID が正しくインストールされているか、PATHが設定されているか確認してください。

### ビルドエラーが発生する

```cmd
cd DroidWpfGui
dotnet restore
dotnet build
```

を実行してパッケージを復元してください。

## 従来のGUIとの比較

| 機能 | Windows Forms版 | WPF版（本バージョン） |
|------|----------------|---------------------|
| デザイン | 標準的 | モダン（ModernWpf） |
| 必須環境 | PowerShell標準 | .NET 8.0 SDK |
| 起動速度 | 高速 | やや遅い（初回ビルド時） |
| カスタマイズ性 | 低 | 高 |
| UI の柔軟性 | 低 | 高 |

## ライセンス

このプロジェクトは ModernWpf ライブラリ（MIT License）を使用しています。
