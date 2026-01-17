#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DROID Desktop GUI - 統合テスト
実際のファイルとの統合をテストします
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
import sys

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPromptJSONIntegration(unittest.TestCase):
    """既存のprompt.jsonとの統合テスト"""
    
    def setUp(self):
        """テスト準備"""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = Path(__file__).parent.parent
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_existing_prompt_json_format(self):
        """既存のprompt.jsonの形式がサポートされているかテスト"""
        prompt_file = self.repo_root / "prompt.json"
        
        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 必須フィールドの確認
            self.assertIn("prompt", data)
            self.assertIn("options", data)
            
            # オプションフィールドの確認
            options = data["options"]
            self.assertIsInstance(options, dict)
    
    def test_create_valid_prompt_json(self):
        """有効なprompt.jsonを作成できるかテスト"""
        test_file = Path(self.test_dir) / "prompt.json"
        
        data = {
            "prompt": "Pythonで計算機アプリを作成して",
            "options": {
                "working_directory": ".",
                "model": "claude-sonnet-4-20250514",
                "auto_level": "medium",
                "log_directory": "logs",
                "ref_filepath": [
                    "./src/main.py"
                ]
            }
        }
        
        # JSONファイルを作成
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # 読み込んで検証
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded["prompt"], data["prompt"])
        self.assertEqual(loaded["options"]["model"], data["options"]["model"])


class TestBatchFileIntegration(unittest.TestCase):
    """バッチファイルとの統合テスト"""
    
    def test_batch_file_content(self):
        """run-droid.batの内容をテスト"""
        bat_file = Path(__file__).parent.parent / "run-droid.bat"
        
        if bat_file.exists():
            with open(bat_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 重要な要素が含まれているか確認
            self.assertIn("python", content.lower())
            self.assertIn("gui_droid.py", content)
            self.assertIn("chcp 65001", content)  # UTF-8設定


class TestPowerShellIntegration(unittest.TestCase):
    """PowerShellスクリプトとの統合テスト"""
    
    def test_powershell_script_exists(self):
        """invoke-droid.ps1が存在するかテスト"""
        ps_file = Path(__file__).parent.parent / "invoke-droid.ps1"
        self.assertTrue(ps_file.exists())
    
    def test_powershell_script_readable(self):
        """invoke-droid.ps1が読み込み可能かテスト"""
        ps_file = Path(__file__).parent.parent / "invoke-droid.ps1"
        
        if ps_file.exists():
            with open(ps_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 重要な要素が含まれているか確認
            self.assertIn("prompt.json", content)
            self.assertIn("droid", content.lower())


class TestDocumentationIntegration(unittest.TestCase):
    """ドキュメントとの統合テスト"""
    
    def test_readme_updated(self):
        """README.mdが更新されているかテスト"""
        readme = Path(__file__).parent.parent / "README.md"
        
        if readme.exists():
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # GUI関連の情報が含まれているか確認
            self.assertIn("GUI", content)
    
    def test_specification_document_exists(self):
        """仕様書が存在するかテスト"""
        spec_file = Path(__file__).parent.parent / "docs" / "GUI仕様書.md"
        self.assertTrue(spec_file.exists(), "GUI仕様書.md が見つかりません")
    
    def test_user_guide_exists(self):
        """使用方法ガイドが存在するかテスト"""
        guide_file = Path(__file__).parent.parent / "docs" / "GUI使用方法.md"
        self.assertTrue(guide_file.exists(), "GUI使用方法.md が見つかりません")


class TestGitignoreIntegration(unittest.TestCase):
    """.gitignoreとの統合テスト"""
    
    def test_gitignore_exists(self):
        """.gitignoreが存在するかテスト"""
        gitignore = Path(__file__).parent.parent / ".gitignore"
        self.assertTrue(gitignore.exists())
    
    def test_gitignore_contains_python_artifacts(self):
        """.gitignoreにPythonの成果物が含まれているかテスト"""
        gitignore = Path(__file__).parent.parent / ".gitignore"
        
        if gitignore.exists():
            with open(gitignore, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Python関連の除外設定があるか確認
            self.assertIn("__pycache__", content)
            # *.py[cod] または *.pyc のいずれかが含まれていればOK
            self.assertTrue("*.py[cod]" in content or "*.pyc" in content)


def run_integration_tests():
    """統合テストを実行"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestPromptJSONIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchFileIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerShellIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestGitignoreIntegration))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
