"""
Pythonの型ヒント使用パターン - 変数定義編
いつ型を明記すべきか、しないべきかの指針
"""

from typing import List, Dict, Optional, Union
from dataclasses import dataclass

# =============================================================================
# 1. 変数の型ヒント - 使うべき場面 vs 使わない場面
# =============================================================================

# ❌ 一般的ではない（型推論が明確な場合）
name: str = "Alice"          # 明らかにstr
age: int = 25               # 明らかにint
is_active: bool = True      # 明らかにbool

# ✅ 推奨される書き方（型推論に任せる）
name = "Alice"              # 型推論でstr
age = 25                   # 型推論でint
is_active = True           # 型推論でbool

# ✅ 型ヒントが有用な場面
user_names: List[str] = []               # 空リストは型推論できない
scores: Dict[str, int] = {}              # 空辞書は型推論できない
current_user: Optional[str] = None       # Noneは型推論できない
# data: Union[str, int] = get_data()     # 複雑な型（例なのでコメントアウト）

# ✅ 複雑な初期化の場合
from typing import DefaultDict
from collections import defaultdict

# 型ヒントがないと何の辞書かわからない
word_count: DefaultDict[str, int] = defaultdict(int)

# =============================================================================
# 2. クラス属性の型ヒント
# =============================================================================

class User:
    """クラス属性の型ヒント例"""
    
    # ✅ クラス変数（共有される）
    total_users: int = 0
    
    def __init__(self, name: str, age: int):
        # ✅ インスタンス変数（型推論が難しい場合）
        self.name = name  # 型推論でstr（型ヒント不要）
        self.age = age    # 型推論でint（型ヒント不要）
        
        # ✅ 後で設定される属性（型ヒント推奨）
        self.email: Optional[str] = None
        self.friends: List[str] = []
        self.metadata: Dict[str, str] = {}

# ✅ dataclassなら型ヒント必須
@dataclass
class Product:
    name: str
    price: float
    tags: List[str]
    metadata: Dict[str, str]

# =============================================================================
# 3. 関数内の変数 - 使い分けパターン
# =============================================================================

def process_user_data(raw_data: List[Dict[str, str]]) -> List[User]:
    """関数内での型ヒント使用例"""
    
    # ❌ 不要（型推論が明確）
    result: List[User] = []
    
    # ✅ 推奨（型推論に任せる）
    result = []  # List[User]は戻り値から推論可能
    
    for item in raw_data:
        # ❌ 不要（型推論が明確）
        name: str = item["name"]
        age_str: str = item["age"]
        
        # ✅ 推奨
        name = item["name"]
        age_str = item["age"]
        
        # ✅ 型変換が関わる場合は有用
        age: int = int(age_str)  # str -> int 変換を明示
        
        result.append(User(name, age))
    
    return result

# =============================================================================
# 4. 複雑な型の場合の型ヒント
# =============================================================================

# ✅ 型エイリアスで可読性向上
UserData = Dict[str, Union[str, int]]
UsersGroup = Dict[str, List[UserData]]

def complex_data_processing():
    """複雑な型の場合は型ヒントが有用"""
    
    # ✅ 複雑な構造の場合
    nested_data: Dict[str, List[Dict[str, Union[str, int]]]] = {
        "users": [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30}
        ]
    }
    
    nested_data_v2: UsersGroup = {
        "users": [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30}
        ]
    }

# =============================================================================
# 5. モジュールレベルの変数
# =============================================================================

# ✅ モジュールレベルの定数
API_VERSION: str = "v1"
MAX_RETRIES: int = 3
DEFAULT_TIMEOUT: float = 30.0

# ✅ 設定値など
config: Dict[str, str] = {
    "database_url": "sqlite:///app.db",
    "secret_key": "your-secret-key"
}

# ✅ 後で初期化される変数
database_connection: Optional[object] = None
cache: Dict[str, str] = {}

# =============================================================================
# 6. 実際のプロジェクトでの使用例
# =============================================================================

class UserService:
    """実際のサービスクラスでの型ヒント使用例"""
    
    def __init__(self):
        # ✅ 初期化時に型が明確でない場合
        self.users: Dict[int, User] = {}
        self.cache: Dict[str, str] = {}
        self.connection: Optional[object] = None
    
    def find_user(self, user_id: int) -> Optional[User]:
        """✅ 関数の引数・戻り値は型ヒント推奨"""
        return self.users.get(user_id)
    
    def process_batch(self, data: List[Dict[str, str]]) -> None:
        """関数内の変数の型ヒント例"""
        
        # ✅ 空のコレクションは型ヒント有用
        processed_users: List[User] = []
        errors: List[str] = []
        
        for item in data:
            try:
                # 型推論に任せる（型ヒント不要）
                name = item.get("name", "")
                age_str = item.get("age", "0")
                
                # 型変換の明示
                age = int(age_str)
                
                user = User(name, age)
                processed_users.append(user)
                
            except ValueError as e:
                errors.append(f"Invalid data: {item}")
        
        # 処理結果を保存
        for user in processed_users:
            self.users[len(self.users)] = user

# =============================================================================
# まとめ：型ヒントを使うべき場面
# =============================================================================

def type_hint_guidelines():
    """
    型ヒントのガイドライン
    
    ✅ 使うべき場面:
    - 関数の引数・戻り値（最重要）
    - 空のコレクション（List, Dict）
    - None の可能性がある変数
    - 複雑な型構造
    - クラス属性（特にdataclass）
    - モジュールレベルの変数
    
    ❌ 使わない場面:
    - 型推論が明確な簡単な代入
    - 関数内のローカル変数（基本的に）
    - 明らかな型変換
    """
    pass

if __name__ == "__main__":
    # 実際の使用例
    users: List[User] = []  # 空リストなので型ヒント有用
    
    # 型推論に任せる
    alice = User("Alice", 25)
    bob = User("Bob", 30)
    
    users.append(alice)
    users.append(bob)
    
    # サービスクラスの使用
    service = UserService()
    service.process_batch([
        {"name": "Charlie", "age": "35"},
        {"name": "David", "age": "40"}
    ])
    
    print(f"Total users: {len(service.users)}")
    print(f"First user: {service.find_user(0)}")
