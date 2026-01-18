#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DROID Desktop GUI - 進捗表示機能のテスト
リアルタイム進捗表示機能をテストします
"""

import unittest
import sys
from pathlib import Path

# 親ディレクトリをパスに追加してgui_droidをインポート可能にする
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestProgressTrackingFeature(unittest.TestCase):
    """進捗表示機能のテスト"""
    
    def setUp(self):
        """テスト準備"""
        self.gui_file = Path(__file__).parent.parent / "gui_droid.py"
        with open(self.gui_file, 'r', encoding='utf-8') as f:
            self.gui_content = f.read()
        
        self.winforms_file = Path(__file__).parent.parent / "gui_droid_winforms.ps1"
        with open(self.winforms_file, 'r', encoding='utf-8') as f:
            self.winforms_content = f.read()
    
    def test_python_gui_has_progress_display(self):
        """Python GUIに進捗表示機能があるかテスト"""
        # ステータステキストエリアが拡張されているか確認
        self.assertIn("実行進捗・ステータス", self.gui_content)
        self.assertIn("height=10", self.gui_content)
    
    def test_python_gui_realtime_output_reading(self):
        """Python GUIがリアルタイム出力読み取りを行うかテスト"""
        # readline()を使用してリアルタイム読み取りをしているか確認
        self.assertIn("readline()", self.gui_content)
        self.assertIn("bufsize=1", self.gui_content)
        
    def test_python_gui_progress_update(self):
        """Python GUIが進捗更新を行うかテスト"""
        # 進捗更新のループがあるか確認
        self.assertIn("while True:", self.gui_content)
        self.assertIn("update_status", self.gui_content)
        self.assertIn("append=True", self.gui_content)
    
    def test_winforms_gui_has_progress_display(self):
        """WinForms GUIに進捗表示機能があるかテスト"""
        # ステータステキストエリアが拡張されているか確認
        self.assertIn("実行進捗・ステータス", self.winforms_content)
        self.assertIn("Size(810, 150)", self.winforms_content)
    
    def test_winforms_gui_realtime_output(self):
        """WinForms GUIがリアルタイム出力を行うかテスト"""
        # リダイレクトとイベントハンドラーの設定があるか確認
        self.assertIn("RedirectStandardOutput", self.winforms_content)
        self.assertIn("OutputDataReceived", self.winforms_content)
        self.assertIn("BeginOutputReadLine", self.winforms_content)
    
    def test_winforms_gui_progress_handler(self):
        """WinForms GUIに進捗ハンドラーがあるかテスト"""
        # 出力イベントハンドラーの定義があるか確認
        self.assertIn("outputHandler", self.winforms_content)
        self.assertIn("AppendText", self.winforms_content)
        self.assertIn("ScrollToCaret", self.winforms_content)
    
    def test_python_gui_thread_safety(self):
        """Python GUIのスレッド安全性テスト"""
        # root.after()を使用してメインスレッドで更新しているか確認
        self.assertIn("self.root.after", self.gui_content)
    
    def test_winforms_gui_thread_safety(self):
        """WinForms GUIのスレッド安全性テスト"""
        # Invoke()を使用してUIスレッドで更新しているか確認
        self.assertIn("Invoke([Action]", self.winforms_content)
    
    def test_status_area_increased_size(self):
        """ステータスエリアのサイズが増加しているかテスト"""
        # Python GUI: height=10 (以前は4)
        self.assertIn("height=10", self.gui_content)
        
        # WinForms GUI: Size 150 (以前は90)
        self.assertIn("Size(810, 150)", self.winforms_content)
    
    def test_form_size_adjusted(self):
        """フォームサイズが調整されているかテスト"""
        # WinForms GUIのサイズが調整されているか確認
        self.assertIn("Size(850, 810)", self.winforms_content)


class TestBackwardCompatibility(unittest.TestCase):
    """後方互換性のテスト"""
    
    def setUp(self):
        """テスト準備"""
        self.gui_file = Path(__file__).parent.parent / "gui_droid.py"
        with open(self.gui_file, 'r', encoding='utf-8') as f:
            self.gui_content = f.read()
    
    def test_original_methods_intact(self):
        """元のメソッドが維持されているかテスト"""
        required_methods = [
            "def __init__",
            "def create_widgets",
            "def load_settings",
            "def save_settings",
            "def execute_droid",
            "def update_status",
            "def _execute_droid_thread"
        ]
        
        for method in required_methods:
            self.assertIn(method, self.gui_content, f"{method} が見つかりません")
    
    def test_security_features_maintained(self):
        """セキュリティ機能が維持されているかテスト"""
        # PowerShellスクリプトパスの検証コードが残っているか確認
        self.assertIn("ps_script.exists()", self.gui_content)
        self.assertIn("samefile", self.gui_content)
    
    def test_error_handling_maintained(self):
        """エラーハンドリングが維持されているかテスト"""
        # try-except-finallyブロックが残っているか確認
        self.assertIn("try:", self.gui_content)
        self.assertIn("except Exception as e:", self.gui_content)
        self.assertIn("finally:", self.gui_content)


def run_tests():
    """テストを実行"""
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestProgressTrackingFeature))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
