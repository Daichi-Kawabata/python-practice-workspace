"""
math_utils.py - 数学関連のユーティリティ

パッケージ内のサブモジュールの例
"""

from typing import Union, List
import math

Number = Union[int, float]

class Calculator:
    """基本的な計算機クラス"""
    
    def __init__(self):
        self.history: List[str] = []
    
    def add(self, a: Number, b: Number) -> Number:
        """加算"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: Number, b: Number) -> Number:
        """減算"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: Number, b: Number) -> Number:
        """乗算"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: Number, b: Number) -> Number:
        """除算"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: Number, exponent: Number) -> Number:
        """べき乗"""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def sqrt(self, x: Number) -> float:
        """平方根"""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(x)
        self.history.append(f"sqrt({x}) = {result}")
        return result
    
    def get_history(self) -> List[str]:
        """計算履歴を取得"""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """計算履歴をクリア"""
        self.history.clear()

def add_numbers(*args: Number) -> Number:
    """複数の数値を合計する関数"""
    if not args:
        return 0
    return sum(args)

def multiply_numbers(*args: Number) -> Number:
    """複数の数値を掛け合わせる関数"""
    if not args:
        return 1
    
    result = 1
    for num in args:
        result *= num
    return result

def factorial(n: int) -> int:
    """階乗を計算"""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def is_prime(n: int) -> bool:
    """素数判定"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

# モジュールレベルの定数
PI = math.pi
E = math.e
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
