"""
Python型システム・型ヒント学習
Ruby/Golangとの比較を含む実践的な例
"""

from typing import List, Dict, Union, Optional, Tuple, Any, Callable
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# 1. 基本的な型ヒント
# =============================================================================

def greet(name: str) -> str:
    """
    基本的な型ヒント
    Go: func greet(name string) string
    Ruby: def greet(name) # 型指定なし（動的型付け）
    """
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    """
    複数パラメータの型ヒント
    Go: func addNumbers(a int, b int) int
    """
    return a + b

def calculate_price(base_price: float, tax_rate: float = 0.08) -> float:
    """
    デフォルト値付きの型ヒント
    Go: 関数のオーバーロードが必要
    Ruby: def calculate_price(base_price, tax_rate = 0.08)
    """
    return base_price * (1 + tax_rate)

# =============================================================================
# 2. コレクション型（List, Dict, Tuple）
# =============================================================================

def process_names(names: List[str]) -> List[str]:
    """
    リスト型の型ヒント
    Go: func processNames(names []string) []string
    Ruby: def process_names(names) # Array<String>はコメントで表現
    """
    return [name.upper() for name in names]

def get_user_scores(users: Dict[str, int]) -> Dict[str, str]:
    """
    辞書型の型ヒント
    Go: func getUserScores(users map[string]int) map[string]string
    Ruby: def get_user_scores(users) # Hash<String, Integer>
    """
    return {name: "Pass" if score >= 60 else "Fail" for name, score in users.items()}

def get_coordinates() -> Tuple[float, float]:
    """
    タプル型の型ヒント（固定長）
    Go: タプルはないため、structを使用
    Ruby: 配列を使用（型チェックなし）
    """
    return (35.6762, 139.6503)  # 東京の緯度経度

# =============================================================================
# 3. Union型とOptional型
# =============================================================================

def format_id(user_id: Union[int, str]) -> str:
    """
    Union型：複数の型を受け入れる
    Go: interface{}を使用するかメソッドオーバーロード
    Ruby: 動的型付けのため型制限なし
    """
    return f"ID: {user_id}"

def find_user(user_id: int) -> Optional[str]:
    """
    Optional型：Noneの可能性がある
    Go: (string, error)のような戻り値パターン
    Ruby: nilを返す可能性がある
    """
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return users.get(user_id)  # Noneを返す可能性

def process_optional_data(data: Optional[List[str]] = None) -> List[str]:
    """
    Optional型のデフォルト値
    """
    if data is None:
        return []
    return [item.upper() for item in data]

# =============================================================================
# 4. 関数型（Callable）
# =============================================================================

def apply_operation(numbers: List[int], operation: Callable[[int], int]) -> List[int]:
    """
    関数を引数として受け取る型ヒント
    Go: func applyOperation(numbers []int, operation func(int) int) []int
    Ruby: def apply_operation(numbers, &block)
    """
    return [operation(num) for num in numbers]

# 使用例
def double(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x ** 2

# =============================================================================
# 5. クラスと型ヒント
# =============================================================================

class User:
    """
    クラスの型ヒント
    """
    def __init__(self, name: str, age: int, email: Optional[str] = None) -> None:
        self.name = name
        self.age = age
        self.email = email
    
    def get_display_name(self) -> str:
        return f"{self.name} ({self.age})"
    
    def update_email(self, email: str) -> None:
        """
        戻り値がない場合はNone
        Go: func (u *User) updateEmail(email string)
        """
        self.email = email

# =============================================================================
# 6. dataclass（Python特有の便利機能）
# =============================================================================

@dataclass
class Product:
    """
    dataclass：自動的に__init__, __repr__などを生成
    Go: structに近い
    Ruby: Structに近い
    """
    name: str
    price: float
    category: str
    in_stock: bool = True
    
    def calculate_total(self, quantity: int) -> float:
        return self.price * quantity

# =============================================================================
# 7. Enum（列挙型）
# =============================================================================

class Status(Enum):
    """
    列挙型
    Go: const ( PENDING = iota; ACTIVE; INACTIVE )
    Ruby: module Status; PENDING = 0; ACTIVE = 1; end
    """
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"

def update_user_status(user: User, status: Status) -> None:
    """
    Enumを型ヒントとして使用
    """
    print(f"User {user.name} status updated to {status.value}")

# =============================================================================
# 8. ジェネリック型（高度な型ヒント）
# =============================================================================

from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    """
    ジェネリック型
    Go: type Stack[T any] struct { items []T }
    Ruby: 型パラメータはサポートされていない
    """
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        if not self._items:
            return None
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        if not self._items:
            return None
        return self._items[-1]

# =============================================================================
# 9. 実践例：型ヒントを活用したAPI関数
# =============================================================================

@dataclass
class ApiResponse:
    status_code: int
    data: Dict[str, Any]
    message: str
    timestamp: datetime

def fetch_user_data(user_id: int, include_email: bool = False) -> ApiResponse:
    """
    実際のAPI関数のような型ヒント
    """
    # 模擬データ
    user_data = {
        "id": user_id,
        "name": "John Doe",
        "age": 30
    }
    
    if include_email:
        user_data["email"] = "john@example.com"
    
    return ApiResponse(
        status_code=200,
        data=user_data,
        message="Success",
        timestamp=datetime.now()
    )

# =============================================================================
# 10. 型チェック用のヘルパー関数
# =============================================================================

def validate_user_input(name: str, age: int, email: Optional[str]) -> bool:
    """
    型ヒントを活用した入力検証
    """
    if not isinstance(name, str) or len(name) == 0:
        return False
    
    if not isinstance(age, int) or age < 0:
        return False
    
    if email is not None and not isinstance(email, str):
        return False
    
    return True

# =============================================================================
# 使用例・テスト
# =============================================================================

if __name__ == "__main__":
    # 基本的な型ヒントのテスト
    print(greet("Python"))
    print(add_numbers(10, 20))
    print(calculate_price(1000.0))
    
    # コレクション型のテスト
    names = ["alice", "bob", "charlie"]
    print(process_names(names))
    
    scores = {"Alice": 85, "Bob": 55, "Charlie": 90}
    print(get_user_scores(scores))
    
    # Union型とOptional型のテスト
    print(format_id(123))
    print(format_id("ABC123"))
    print(find_user(1))
    print(find_user(999))  # None
    
    # 関数型のテスト
    numbers = [1, 2, 3, 4, 5]
    print(apply_operation(numbers, double))
    print(apply_operation(numbers, square))
    
    # クラスのテスト
    user = User("Alice", 25, "alice@example.com")
    print(user.get_display_name())
    
    # dataclassのテスト
    product = Product("Laptop", 999.99, "Electronics")
    print(product)
    print(product.calculate_total(2))
    
    # Enumのテスト
    update_user_status(user, Status.ACTIVE)
    
    # ジェネリック型のテスト
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(int_stack.pop())  # 2
    
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(str_stack.pop())  # "world"
    
    # API関数のテスト
    response = fetch_user_data(123, include_email=True)
    print(response)
    
    # 入力検証のテスト
    print(validate_user_input("Alice", 25, "alice@example.com"))  # True
    print(validate_user_input("", 25, None))  # False
