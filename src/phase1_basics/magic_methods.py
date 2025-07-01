"""
Pythonのマジックメソッド（特殊メソッド）の理解
__init__, __repr__, __str__ などの詳細解説
"""

from dataclasses import dataclass
from typing import Optional

# =============================================================================
# 1. __init__ メソッド（コンストラクタ）
# =============================================================================

class User:
    """通常のクラス定義での__init__の使用例"""
    
    def __init__(self, name: str, age: int, email: Optional[str] = None):
        """
        __init__: オブジェクトの初期化メソッド（コンストラクタ）
        
        Go: func NewUser(name string, age int, email *string) *User
        Ruby: def initialize(name, age, email = nil)
        """
        print(f"Creating user: {name}")  # 初期化時に実行される
        self.name = name      # インスタンス変数に値を設定
        self.age = age
        self.email = email
        self.created_at = "2025-07-01"  # 初期化時に自動設定

# =============================================================================
# 2. __repr__ メソッド（開発者向け文字列表現）
# =============================================================================

class UserWithRepr:
    """__repr__を定義したクラス"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self) -> str:
        """
        __repr__: オブジェクトの「公式な」文字列表現
        - 開発者がデバッグ時に見るためのもの
        - 理想的には eval(repr(obj)) == obj となるような文字列
        """
        return f"UserWithRepr(name='{self.name}', age={self.age})"

class UserWithoutRepr:
    """__repr__を定義していないクラス"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# =============================================================================
# 3. __str__ メソッド（ユーザー向け文字列表現）
# =============================================================================

class UserWithStr:
    """__str__を定義したクラス"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self) -> str:
        """開発者向け表現"""
        return f"UserWithStr(name='{self.name}', age={self.age})"
    
    def __str__(self) -> str:
        """
        __str__: オブジェクトの「ユーザーフレンドリーな」文字列表現
        - エンドユーザーが見るためのもの
        - print()や str()で使用される
        """
        return f"{self.name} (Age: {self.age})"

# =============================================================================
# 4. dataclassの自動生成機能
# =============================================================================

@dataclass
class ProductWithDataclass:
    """
    dataclass: __init__, __repr__, __eq__ などを自動生成
    """
    name: str
    price: float
    category: str
    in_stock: bool = True
    
    # 自動生成されるメソッド例:
    # def __init__(self, name: str, price: float, category: str, in_stock: bool = True):
    #     self.name = name
    #     self.price = price
    #     self.category = category
    #     self.in_stock = in_stock
    #
    # def __repr__(self) -> str:
    #     return f"ProductWithDataclass(name='{self.name}', price={self.price}, category='{self.category}', in_stock={self.in_stock})"

# 通常のクラスで同じことを実装すると...
class ProductWithoutDataclass:
    """dataclassを使わない場合の手動実装"""
    
    def __init__(self, name: str, price: float, category: str, in_stock: bool = True):
        self.name = name
        self.price = price
        self.category = category
        self.in_stock = in_stock
    
    def __repr__(self) -> str:
        return f"ProductWithoutDataclass(name='{self.name}', price={self.price}, category='{self.category}', in_stock={self.in_stock})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ProductWithoutDataclass):
            return False
        return (self.name == other.name and 
                self.price == other.price and 
                self.category == other.category and 
                self.in_stock == other.in_stock)

# =============================================================================
# 5. 他の重要なマジックメソッド
# =============================================================================

class BankAccount:
    """様々なマジックメソッドの実装例"""
    
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
    
    def __repr__(self) -> str:
        """開発者向け表現"""
        return f"BankAccount(owner='{self.owner}', balance={self.balance})"
    
    def __str__(self) -> str:
        """ユーザー向け表現"""
        return f"{self.owner}'s account: ${self.balance:.2f}"
    
    def __eq__(self, other) -> bool:
        """== 演算子の動作を定義"""
        if not isinstance(other, BankAccount):
            return False
        return self.owner == other.owner and self.balance == other.balance
    
    def __lt__(self, other) -> bool:
        """< 演算子の動作を定義（残高で比較）"""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance
    
    def __add__(self, amount: float) -> 'BankAccount':
        """+ 演算子の動作を定義（残高に加算）"""
        return BankAccount(self.owner, self.balance + amount)
    
    def __len__(self) -> int:
        """len()関数の動作を定義（残高の桁数）"""
        return len(str(int(self.balance)))

# =============================================================================
# 実際の使用例とテスト
# =============================================================================

def test_magic_methods():
    """マジックメソッドの動作確認"""
    
    print("=== __init__ の動作 ===")
    user1 = User("Alice", 25)  # __init__が呼ばれる
    print(f"User created: {user1.name}, {user1.age}, {user1.created_at}")
    
    print("\n=== __repr__ の比較 ===")
    # __repr__あり
    user_with_repr = UserWithRepr("Bob", 30)
    print(f"repr()で表示: {repr(user_with_repr)}")
    print(f"print()で表示: {user_with_repr}")  # __str__がない場合は__repr__が使われる
    
    # __repr__なし
    user_without_repr = UserWithoutRepr("Charlie", 35)
    print(f"repr()で表示: {repr(user_without_repr)}")  # デフォルトの表現
    
    print("\n=== __str__ vs __repr__ ===")
    user_with_str = UserWithStr("David", 40)
    print(f"repr()で表示: {repr(user_with_str)}")  # __repr__が使われる
    print(f"str()で表示: {str(user_with_str)}")    # __str__が使われる
    print(f"print()で表示: {user_with_str}")       # __str__が使われる
    
    print("\n=== dataclass vs 通常のクラス ===")
    # dataclass
    product1 = ProductWithDataclass("Laptop", 999.99, "Electronics")
    print(f"dataclass: {product1}")
    
    # 通常のクラス
    product2 = ProductWithoutDataclass("Laptop", 999.99, "Electronics")
    print(f"通常のクラス: {product2}")
    
    print("\n=== その他のマジックメソッド ===")
    account1 = BankAccount("Alice", 1000.0)
    account2 = BankAccount("Bob", 1500.0)
    
    print(f"repr: {repr(account1)}")
    print(f"str: {str(account1)}")
    print(f"等価性: {account1 == account2}")  # __eq__
    print(f"比較: {account1 < account2}")     # __lt__
    print(f"加算: {account1 + 500}")          # __add__
    print(f"長さ: {len(account1)}")           # __len__

# =============================================================================
# Ruby/Golangとの比較
# =============================================================================

def language_comparison():
    """他言語との比較"""
    
    print("\n=== 言語比較 ===")
    
    # Python
    user = UserWithRepr("Alice", 25)
    print(f"Python: {user}")
    
    # Go equivalent:
    # type User struct {
    #     Name string
    #     Age  int
    # }
    # func NewUser(name string, age int) *User {
    #     return &User{Name: name, Age: age}
    # }
    # func (u User) String() string {
    #     return fmt.Sprintf("User{Name: %s, Age: %d}", u.Name, u.Age)
    # }
    
    # Ruby equivalent:
    # class User
    #   def initialize(name, age)
    #     @name = name
    #     @age = age
    #   end
    #   
    #   def to_s
    #     "User(name: #{@name}, age: #{@age})"
    #   end
    # end

if __name__ == "__main__":
    test_magic_methods()
    language_comparison()
