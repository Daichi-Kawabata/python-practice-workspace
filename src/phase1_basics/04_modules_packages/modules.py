"""
Pythonモジュール・パッケージ学習
他言語（Ruby/Go）との比較を含む実践的な解説

学習項目:
1. モジュール（.pyファイル）の作成・インポート
2. パッケージ（ディレクトリ）の作成・__init__.py
3. from/import文の使い分け
4. 相対インポート vs 絶対インポート
5. __name__ == "__main__" の詳細
6. モジュール検索パス
7. サードパーティパッケージの管理
"""

import sys
import os
from pathlib import Path

# =============================================================================
# 1. モジュールの基本概念
# =============================================================================

def module_basics():
    """
    モジュールの基本概念
    
    Python: 1つの.pyファイル = 1つのモジュール
    Ruby: require 'file_name' でファイルを読み込み
    Go: package システムでファイル群をまとめる
    """
    
    print("=== モジュール基本情報 ===")
    print(f"現在のモジュール名: {__name__}")
    print(f"現在のファイルパス: {__file__}")
    print(f"現在のディレクトリ: {os.path.dirname(__file__)}")
    
    # モジュール検索パス
    print(f"\nPython モジュール検索パス:")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")

# =============================================================================
# 2. インポートの方法
# =============================================================================

def import_examples():
    """
    各種インポート方法の例
    """
    
    # 標準ライブラリ
    import json
    import datetime
    from collections import defaultdict
    from pathlib import Path
    
    # エイリアス（例 - 実際にインストールが必要）
    # import numpy as np  # 慣例的なエイリアス
    # import pandas as pd
    
    # 特定の関数・クラスのみ
    from datetime import datetime, timedelta
    from typing import List, Dict, Optional
    
    print("=== インポート例 ===")
    
    # json モジュール使用例
    data = {"name": "Python", "version": "3.11"}
    json_str = json.dumps(data)
    print(f"JSON変換: {json_str}")
    
    # datetime 使用例
    now = datetime.now()
    print(f"現在時刻: {now}")
    
    # pathlib 使用例
    current_path = Path(__file__).parent
    print(f"現在のディレクトリ: {current_path}")

# =============================================================================
# 3. カスタムモジュールの例
# =============================================================================

# このファイル自体がモジュールとして機能する

class Calculator:
    """計算機クラス（モジュール内で定義）"""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """加算"""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """減算"""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """乗算"""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """除算"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

def greet(name: str) -> str:
    """挨拶関数（モジュール内で定義）"""
    return f"Hello, {name}!"

# モジュールレベルの変数（定数）
VERSION = "1.0.0"
AUTHOR = "Python学習者"

# =============================================================================
# 4. __name__ == "__main__" の詳細解説
# =============================================================================

def main_explanation():
    """
    __name__ == "__main__" の詳細解説
    
    Python: スクリプトとして実行された場合のみTrue
    Ruby: if __FILE__ == $0 に相当
    Go: main packageのmain()関数が自動実行
    """
    
    print("=== __name__ の動作確認 ===")
    print(f"現在の __name__: {__name__}")
    
    if __name__ == "__main__":
        print("このファイルは直接実行されました")
        print("メイン処理を開始します")
    else:
        print("このファイルはモジュールとしてインポートされました")

# =============================================================================
# 5. モジュールの属性とメタ情報
# =============================================================================

def module_attributes():
    """モジュールの属性・メタ情報"""
    
    print("=== モジュール属性 ===")
    
    # モジュール内の全ての名前を取得
    module_names = dir()
    print(f"モジュール内の名前一覧:")
    for name in sorted(module_names):
        if not name.startswith('_'):
            print(f"  {name}")
    
    # 特定の属性の確認
    print(f"\nモジュール属性:")
    print(f"  __name__: {__name__}")
    print(f"  __file__: {__file__}")
    print(f"  __doc__: {__doc__[:50]}..." if __doc__ else "None")
    
    # グローバル変数の確認
    print(f"\nグローバル変数:")
    print(f"  VERSION: {VERSION}")
    print(f"  AUTHOR: {AUTHOR}")

# =============================================================================
# 6. 動的インポート
# =============================================================================

def dynamic_import_example():
    """動的インポートの例"""
    
    print("=== 動的インポート ===")
    
    # importlib を使用した動的インポート
    import importlib
    
    # モジュール名を文字列で指定
    module_name = "json"
    json_module = importlib.import_module(module_name)
    
    data = {"dynamic": True}
    result = json_module.dumps(data)
    print(f"動的インポートでJSON変換: {result}")
    
    # 関数の動的取得
    func_name = "loads"
    loads_func = getattr(json_module, func_name)
    parsed = loads_func(result)
    print(f"動的に取得した関数で解析: {parsed}")

# =============================================================================
# 7. モジュール検索パスの操作
# =============================================================================

def path_manipulation():
    """モジュール検索パスの操作"""
    
    print("=== パス操作 ===")
    
    # 現在のパス状況
    print(f"現在の作業ディレクトリ: {os.getcwd()}")
    print(f"スクリプトのディレクトリ: {os.path.dirname(__file__)}")
    
    # パスを追加（実際にはやらない、例として）
    script_dir = os.path.dirname(__file__)
    if script_dir not in sys.path:
        print(f"パスに追加する場合: {script_dir}")
        # sys.path.insert(0, script_dir)  # 最優先で検索
        # sys.path.append(script_dir)     # 最後に検索

# =============================================================================
# 8. 他言語との比較
# =============================================================================

def language_comparison():
    """他言語との比較"""
    
    print("=== 言語比較 ===")
    
    print("""
Python モジュール・パッケージ:
- 1つの.pyファイル = 1つのモジュール
- ディレクトリ + __init__.py = パッケージ
- import文でモジュールを読み込み
- 相対インポート/絶対インポート

Ruby モジュール・ライブラリ:
- require 'filename' でファイル読み込み
- module キーワードで名前空間作成
- gem でパッケージ管理
- load_path で検索パス設定

Go パッケージシステム:
- package宣言でパッケージ名指定
- import "package/path" で読み込み
- go.mod でモジュール管理
- 大文字開始で公開、小文字開始で非公開
""")

# =============================================================================
# 使用例・テスト
# =============================================================================

def run_examples():
    """全ての例を実行"""
    
    module_basics()
    print("\n" + "="*50)
    
    import_examples()
    print("\n" + "="*50)
    
    # Calculator クラスのテスト
    calc = Calculator()
    print("=== Calculator テスト ===")
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"10 - 5 = {calc.subtract(10, 5)}")
    print(f"10 * 5 = {calc.multiply(10, 5)}")
    print(f"10 / 5 = {calc.divide(10, 5)}")
    
    # greet 関数のテスト
    print(f"\n挨拶: {greet('Python学習者')}")
    
    print("\n" + "="*50)
    main_explanation()
    
    print("\n" + "="*50)
    module_attributes()
    
    print("\n" + "="*50)
    dynamic_import_example()
    
    print("\n" + "="*50)
    path_manipulation()
    
    print("\n" + "="*50)
    language_comparison()

if __name__ == "__main__":
    print("モジュール・パッケージ学習開始")
    print("="*60)
    run_examples()
    print("="*60)
    print("学習完了")
