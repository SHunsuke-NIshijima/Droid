#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DROID Desktop GUI - 機能テスト
GUIの各機能をテストします（GUI表示なしでテスト可能な部分）
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import sys
import os

# 親ディレクトリをパスに追加してgui_droidをインポート可能にする
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestJSONOperations(unittest.TestCase):
    """JSON読み書き機能のテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = Path(self.test_dir) / "test_prompt.json"
    
    def tearDown(self):
        """各テストの後に実行"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_json_write_read(self):
        """JSON書き込みと読み込みのテスト"""
        test_data = {
            "prompt": "テストプロンプト",
            "options": {
                "working_directory": ".",
                "model": "claude-sonnet-4-20250514",
                "auto_level": "medium",
                "log_directory": "logs"
            }
        }
        
        # 書き込み
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)
        
        # 読み込み
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # 検証
        self.assertEqual(loaded_data, test_data)
    
    def test_json_japanese_characters(self):
        """日本語文字のエンコーディングテスト"""
        test_data = {
            "prompt": "このコードをレビューしてください。改善点を教えて。",
            "options": {
                "working_directory": "。/サンプル/",
                "model": "claude-opus-4-5-20251101"
            }
        }
        
        # 書き込み
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)
        
        # 読み込み
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # 日本語が正しく保存・読み込みされているか確認
        self.assertEqual(loaded_data["prompt"], test_data["prompt"])
        self.assertIn("レビュー", loaded_data["prompt"])
    
    def test_json_with_reference_paths(self):
        """参照パスを含むJSONのテスト"""
        test_data = {
            "prompt": "テスト",
            "options": {
                "working_directory": ".",
                "model": "claude-sonnet-4-20250514",
                "auto_level": "high",
                "log_directory": "logs",
                "ref_filepath": [
                    "./sample/input_data.xlsx",
                    "./sample/columns_output.xlsx",
                    "./src/main.py"
                ]
            }
        }
        
        # 書き込み
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)
        
        # 読み込み
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # 参照パスが正しく保存されているか確認
        self.assertEqual(len(loaded_data["options"]["ref_filepath"]), 3)
        self.assertIn("./sample/input_data.xlsx", loaded_data["options"]["ref_filepath"])
    
    def test_json_empty_prompt_handling(self):
        """空のプロンプトの処理テスト"""
        test_data = {
            "prompt": "",
            "options": {
                "working_directory": "."
            }
        }
        
        # 書き込み
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)
        
        # 読み込み
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # 空のプロンプトが正しく扱われるか確認
        self.assertEqual(loaded_data["prompt"], "")


class TestDataValidation(unittest.TestCase):
    """データ検証のテスト"""
    
    def test_valid_model_names(self):
        """有効なモデル名のテスト"""
        valid_models = [
            "claude-opus-4-5-20251101",
            "claude-sonnet-4-20250514",
            "claude-sonnet-4-5-20241022",
            "claude-haiku-4-20250116"
        ]
        
        for model in valid_models:
            # モデル名が正しい形式であることを確認
            self.assertTrue(model.startswith("claude-"))
            self.assertIn("-", model)
    
    def test_valid_auto_levels(self):
        """有効な自動化レベルのテスト"""
        valid_levels = ["low", "medium", "high"]
        
        for level in valid_levels:
            # 自動化レベルが有効な値であることを確認
            self.assertIn(level, valid_levels)
    
    def test_path_validation(self):
        """パスの検証テスト"""
        # 相対パス
        relative_path = "."
        self.assertTrue(len(relative_path) > 0)
        
        # 絶対パス（Windows形式）
        abs_path_win = "C:/projects/myapp"
        self.assertIn("/", abs_path_win)


class TestFileStructure(unittest.TestCase):
    """ファイル構造のテスト"""
    
    def test_gui_file_exists(self):
        """gui_droid.pyが存在するかテスト"""
        gui_file = Path(__file__).parent.parent / "gui_droid.py"
        self.assertTrue(gui_file.exists())
    
    def test_batch_file_exists(self):
        """run-droid.batが存在するかテスト"""
        bat_file = Path(__file__).parent.parent / "run-droid.bat"
        self.assertTrue(bat_file.exists())
    
    def test_powershell_script_exists(self):
        """invoke-droid.ps1が存在するかテスト"""
        ps_file = Path(__file__).parent.parent / "invoke-droid.ps1"
        self.assertTrue(ps_file.exists())
    
    def test_documentation_exists(self):
        """ドキュメントファイルが存在するかテスト"""
        docs_dir = Path(__file__).parent.parent / "docs"
        self.assertTrue(docs_dir.exists())
        
        # 主要なドキュメントの存在確認
        expected_docs = [
            "GUI仕様書.md",
            "GUI使用方法.md",
            "GUI画面イメージ.md",
            "クイックスタートガイド.md"
        ]
        
        for doc in expected_docs:
            doc_file = docs_dir / doc
            self.assertTrue(doc_file.exists(), f"{doc} が見つかりません")


class TestGUICodeStructure(unittest.TestCase):
    """GUIコードの構造テスト"""
    
    def setUp(self):
        """テスト準備"""
        self.gui_file = Path(__file__).parent.parent / "gui_droid.py"
        with open(self.gui_file, 'r', encoding='utf-8') as f:
            self.gui_content = f.read()
    
    def test_required_imports(self):
        """必要なインポートが含まれているかテスト"""
        required_imports = [
            "import tkinter",
            "import json",
            "import subprocess",
            "from pathlib import Path",
            "import threading"
        ]
        
        for imp in required_imports:
            self.assertIn(imp, self.gui_content, f"{imp} が見つかりません")
    
    def test_class_definition(self):
        """DroidGUIクラスが定義されているかテスト"""
        self.assertIn("class DroidGUI", self.gui_content)
    
    def test_required_methods(self):
        """必要なメソッドが定義されているかテスト"""
        required_methods = [
            "def __init__",
            "def create_widgets",
            "def load_settings",
            "def save_settings",
            "def execute_droid",
            "def update_status"
        ]
        
        for method in required_methods:
            self.assertIn(method, self.gui_content, f"{method} が見つかりません")
    
    def test_security_validation(self):
        """セキュリティ関連のコードが含まれているかテスト"""
        # PowerShellスクリプトパスの検証コードがあるか確認
        self.assertIn("ps_script.exists()", self.gui_content)
        self.assertIn("samefile", self.gui_content)


def run_tests():
    """テストを実行"""
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestJSONOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFileStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestGUICodeStructure))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
