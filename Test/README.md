# DROID Desktop GUI - テストスイート

このフォルダには、DROID Desktop GUIアプリケーションの自動テストが含まれています。

## テストファイル

### 1. `test_gui_functionality.py`
GUIの各機能をテストします（GUI表示なしでテスト可能な部分）

#### テストクラス：
- **TestJSONOperations**: JSON読み書き機能のテスト
  - JSON書き込みと読み込み
  - 日本語文字のエンコーディング
  - 参照パスを含むJSON
  - 空のプロンプトの処理

- **TestDataValidation**: データ検証のテスト
  - 有効なモデル名
  - 有効な自動化レベル
  - パスの検証

- **TestFileStructure**: ファイル構造のテスト
  - 必要なファイルの存在確認
  - ドキュメントファイルの存在確認

- **TestGUICodeStructure**: GUIコードの構造テスト
  - 必要なインポート
  - クラスとメソッドの定義
  - セキュリティ機能の実装確認

### 2. `test_integration.py`
実際のファイルとの統合をテストします

#### テストクラス：
- **TestPromptJSONIntegration**: 既存のprompt.jsonとの統合テスト
- **TestBatchFileIntegration**: バッチファイルとの統合テスト
- **TestPowerShellIntegration**: PowerShellスクリプトとの統合テスト
- **TestDocumentationIntegration**: ドキュメントとの統合テスト
- **TestGitignoreIntegration**: .gitignoreとの統合テスト

### 3. `run_all_tests.py`
全てのテストを実行するためのテストランナー

## テストの実行方法

### 全てのテストを実行
```bash
cd /path/to/Droid
python Test/run_all_tests.py
```

### 機能テストのみ実行
```bash
cd /path/to/Droid
python Test/test_gui_functionality.py
```

### 統合テストのみ実行
```bash
cd /path/to/Droid
python Test/test_integration.py
```

### Windowsの場合
```cmd
cd C:\path\to\Droid
python Test\run_all_tests.py
```

## テスト結果の見方

### 成功した場合
```
...
----------------------------------------------------------------------
Ran 25 tests in 0.123s

OK

✓ 全てのテストが成功しました！
```

### 失敗した場合
```
...
======================================================================
FAIL: test_xxx (Test.test_gui_functionality.TestXXX)
----------------------------------------------------------------------
...

----------------------------------------------------------------------
Ran 25 tests in 0.123s

FAILED (failures=1)

✗ いくつかのテストが失敗しました
```

## テストのカバレッジ

以下の領域がテストされています：

1. **JSON操作**
   - ファイルの読み書き
   - UTF-8エンコーディング
   - 日本語文字の処理

2. **データ検証**
   - モデル名の妥当性
   - 自動化レベルの妥当性
   - パスの検証

3. **ファイル構造**
   - 必要なファイルの存在
   - ドキュメントの完全性

4. **コード品質**
   - 必要なインポート
   - クラスとメソッドの存在
   - セキュリティ機能の実装

5. **統合**
   - 既存ファイルとの互換性
   - バッチファイルとの連携
   - PowerShellスクリプトとの連携

## 前提条件

- Python 3.8以上
- 標準ライブラリのみ（追加のインストール不要）

## トラブルシューティング

### ImportError: No module named 'Test'
→ プロジェクトのルートディレクトリから実行してください

### FileNotFoundError
→ 必要なファイル（gui_droid.py、prompt.jsonなど）が存在するか確認してください

### テストが失敗する
→ テストの出力を確認し、どのテストが失敗しているかを特定してください
→ 失敗の詳細情報がエラーメッセージに表示されます

## 新しいテストの追加

新しいテストを追加する場合：

1. `test_*.py`という名前で新しいファイルを作成
2. `unittest.TestCase`を継承したテストクラスを作成
3. `test_`で始まるメソッドを追加
4. `run_all_tests.py`に新しいテストモジュールをインポート

例：
```python
import unittest

class TestNewFeature(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)
```

## CI/CD統合

これらのテストは、CI/CDパイプラインに統合することができます：

```yaml
# GitHub Actions の例
- name: Run tests
  run: python Test/run_all_tests.py
```

## ライセンス

このテストスイートは、DROID Desktop GUIプロジェクトと同じライセンスの下でライセンスされています。
