"""
パッケージインポートのテスト

sample_packageの各種インポート方法を実践
"""

import sys
import os

# 現在のディレクトリをPythonパスに追加（必要に応じて）
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("=== パッケージインポートテスト ===")

# 1. パッケージ全体のインポート
print("\n1. パッケージ全体のインポート")
import sample_package
print(f"パッケージバージョン: {sample_package.__version__}")
print(f"パッケージ作者: {sample_package.__author__}")
print(f"パッケージ説明: {sample_package.__description__}")

# パッケージレベル関数の使用
greeting = sample_package.greet("テスト")
print(f"パッケージレベル関数: {greeting}")

# 2. 特定のクラス・関数のインポート
print("\n2. 特定のクラス・関数のインポート")
from sample_package import Calculator, StringUtil, Logger, add_numbers

# Calculator のテスト
calc = Calculator()
print(f"10 + 5 = {calc.add(10, 5)}")
print(f"10 * 3 = {calc.multiply(10, 3)}")
print(f"計算履歴: {calc.get_history()}")

# StringUtil のテスト
text = "Hello, World!"
print(f"文字列: '{text}'")
print(f"逆順: '{StringUtil.reverse(text)}'")
print(f"単語数: {StringUtil.count_words(text)}")
print(f"回文判定 'racecar': {StringUtil.is_palindrome('racecar')}")

# add_numbers のテスト
sum_result = add_numbers(1, 2, 3, 4, 5)
print(f"数値の合計: {sum_result}")

# 3. サブモジュールの直接インポート
print("\n3. サブモジュールの直接インポート")
from sample_package.math_utils import factorial, is_prime
from sample_package.string_utils import levenshtein_distance, similarity_ratio

print(f"5の階乗: {factorial(5)}")
print(f"13は素数?: {is_prime(13)}")
print(f"17は素数?: {is_prime(17)}")

print(f"'kitten'と'sitting'のレーベンシュタイン距離: {levenshtein_distance('kitten', 'sitting')}")
print(f"'kitten'と'sitting'の類似度: {similarity_ratio('kitten', 'sitting'):.2f}")

# 4. エイリアス付きインポート
print("\n4. エイリアス付きインポート")
from sample_package.math_utils import Calculator as MathCalc
from sample_package.string_utils import StringUtil as StrUtil

math_calc = MathCalc()
result = math_calc.power(2, 8)
print(f"2の8乗: {result}")

camel_case = StrUtil.snake_to_camel("hello_world_python")
print(f"snake_to_camel: {camel_case}")

# 5. ワイルドカードインポート（__all__で制御）
print("\n5. ワイルドカードインポート")
# from sample_package import *  # 実際にはやらない（例として）
# 理由: 名前空間の汚染を防ぐため

# 6. ロガーのテスト
print("\n6. ロガーのテスト")
logger = Logger("test_logger")
logger.info("これは情報ログです")
logger.warning("これは警告ログです")
logger.debug("これはデバッグログです（表示されない可能性があります）")

# パフォーマンスロガーのテスト
from sample_package.logging_utils import PerformanceLogger
import time

with PerformanceLogger(logger, "heavy_operation"):
    time.sleep(0.1)  # 重い処理をシミュレート

# 7. モジュール情報の確認
print("\n7. モジュール情報の確認")
print(f"sample_package.__name__: {sample_package.__name__}")
print(f"sample_package.__file__: {sample_package.__file__}")
print(f"sample_package.__all__: {sample_package.__all__}")

# 8. 動的インポート
print("\n8. 動的インポート")
import importlib

# モジュールを動的にインポート
math_utils = importlib.import_module('sample_package.math_utils')
dynamic_calc = math_utils.Calculator()
print(f"動的インポートでの計算: {dynamic_calc.add(100, 200)}")

# 9. インポートエラーの処理
print("\n9. インポートエラーの処理")
try:
    from sample_package import NonExistentClass  # type: ignore # 意図的なエラー
except ImportError as e:
    print(f"インポートエラー: {e}")

try:
    import non_existent_module  # type: ignore # 意図的なエラー
except ImportError as e:
    print(f"モジュールが見つかりません: {e}")

print("\n=== テスト完了 ===")
