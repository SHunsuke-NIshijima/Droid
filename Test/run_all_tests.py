#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DROID Desktop GUI - テストランナー
全てのテストを実行します
"""

import sys
import unittest
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# テストモジュールをインポート
from Test import test_gui_functionality
from Test import test_integration


def run_all_tests():
    """全てのテストを実行"""
    print("=" * 70)
    print("DROID Desktop GUI - テストスイート")
    print("=" * 70)
    print()
    
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 機能テストを追加
    print("機能テストを読み込み中...")
    suite.addTests(loader.loadTestsFromModule(test_gui_functionality))
    
    # 統合テストを追加
    print("統合テストを読み込み中...")
    suite.addTests(loader.loadTestsFromModule(test_integration))
    
    print()
    print("=" * 70)
    print("テスト実行開始")
    print("=" * 70)
    print()
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 結果サマリー
    print()
    print("=" * 70)
    print("テスト結果サマリー")
    print("=" * 70)
    print(f"実行したテスト数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("✓ 全てのテストが成功しました！")
        print("=" * 70)
        return 0
    else:
        print()
        print("✗ いくつかのテストが失敗しました")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
