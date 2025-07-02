"""
sample_package パッケージの初期化ファイル

__init__.py ファイルの役割:
1. ディレクトリをPythonパッケージとして認識させる
2. パッケージレベルの初期化処理
3. 外部に公開する名前の制御
4. パッケージの簡単な説明やメタデータ
"""

# パッケージ情報
__version__ = "1.0.0"
__author__ = "Python学習者"
__description__ = "モジュール学習用のサンプルパッケージ"

# 外部に公開するモジュール・クラス・関数を明示
# これらは from sample_package import * でインポートされる
__all__ = [
    'Calculator',
    'StringUtil', 
    'Logger',
    'greet',
    'add_numbers'
]

# サブモジュールから重要なクラス・関数をインポート
from .math_utils import Calculator, add_numbers
from .string_utils import StringUtil
from .logging_utils import Logger

# パッケージレベル関数
def greet(name: str) -> str:
    """パッケージレベルの挨拶関数"""
    return f"Hello from sample_package, {name}!"

# パッケージ初期化時の処理
print(f"sample_package v{__version__} initialized")
