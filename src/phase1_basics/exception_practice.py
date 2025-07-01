"""
例外処理の実践練習
実際のアプリケーションで起こりうるシナリオを想定した練習問題
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

# =============================================================================
# 練習1: ファイル操作と例外処理
# =============================================================================

class FileProcessingError(Exception):
    """ファイル処理専用の例外"""
    def __init__(self, filepath: str, operation: str, original_error: Exception):
        self.filepath = filepath
        self.operation = operation
        self.original_error = original_error
        super().__init__(f"Failed to {operation} file '{filepath}': {original_error}")

class ConfigManager:
    """設定ファイル管理クラス（例外処理の実践）"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return self.config
        except FileNotFoundError as e:
            raise FileProcessingError(str(self.config_path), "read", e)
        except json.JSONDecodeError as e:
            raise FileProcessingError(str(self.config_path), "parse JSON", e)
        except PermissionError as e:
            raise FileProcessingError(str(self.config_path), "access", e)
        except Exception as e:
            raise FileProcessingError(str(self.config_path), "process", e)
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """設定ファイルを保存する"""
        try:
            # ディレクトリが存在しない場合は作成
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.config = config
            
        except PermissionError as e:
            raise FileProcessingError(str(self.config_path), "write", e)
        except Exception as e:
            raise FileProcessingError(str(self.config_path), "save", e)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """設定値を取得する"""
        try:
            return self.config[key]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Setting '{key}' not found in config")

# =============================================================================
# 練習2: ネットワーク操作とリトライ機能
# =============================================================================

class NetworkError(Exception):
    """ネットワーク関連エラー"""
    pass

class APIClient:
    """API クライアント（リトライ機能付き）"""
    
    def __init__(self, base_url: str, max_retries: int = 3):
        self.base_url = base_url
        self.max_retries = max_retries
    
    def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        """データを取得（リトライ機能付き）"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # 実際のHTTPリクエストの代わりにシミュレーション
                return self._simulate_api_call(endpoint, attempt)
                
            except NetworkError as e:
                last_error = e
                print(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {2 ** attempt} seconds...")
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print("Max retries exceeded")
        
        # すべてのリトライが失敗した場合
        raise NetworkError(f"Failed to fetch data after {self.max_retries} attempts") from last_error
    
    def _simulate_api_call(self, endpoint: str, attempt: int) -> Dict[str, Any]:
        """API呼び出しのシミュレーション"""
        import random
        
        # 最初の2回は失敗させる（リトライのテスト）
        if attempt < 2:
            error_types = [
                ("Connection timeout", NetworkError("Connection timeout")),
                ("Server error", NetworkError("Internal server error")),
                ("Rate limit", NetworkError("Rate limit exceeded"))
            ]
            error_name, error = random.choice(error_types)
            raise error
        
        # 3回目は成功
        return {
            "endpoint": endpoint,
            "data": f"Success data from {endpoint}",
            "timestamp": datetime.now().isoformat(),
            "attempt": attempt + 1
        }

# =============================================================================
# 練習3: データベース操作と トランザクション
# =============================================================================

class DatabaseError(Exception):
    """データベース関連エラー"""
    pass

class TransactionError(DatabaseError):
    """トランザクション関連エラー"""
    pass

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    created_at: Optional[datetime] = None

class DatabaseManager:
    """データベース管理クラス（トランザクション処理）"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.next_id = 1
        self.in_transaction = False
        self.transaction_backup: Optional[Dict[int, User]] = None
    
    def begin_transaction(self):
        """トランザクション開始"""
        if self.in_transaction:
            raise TransactionError("Transaction already in progress")
        
        self.in_transaction = True
        self.transaction_backup = self.users.copy()
        print("Transaction started")
    
    def commit_transaction(self):
        """トランザクションコミット"""
        if not self.in_transaction:
            raise TransactionError("No transaction in progress")
        
        self.in_transaction = False
        self.transaction_backup = None
        print("Transaction committed")
    
    def rollback_transaction(self):
        """トランザクションロールバック"""
        if not self.in_transaction:
            raise TransactionError("No transaction in progress")
        
        if self.transaction_backup is not None:
            self.users = self.transaction_backup
        
        self.in_transaction = False
        self.transaction_backup = None
        print("Transaction rolled back")
    
    def create_user(self, name: str, email: str) -> User:
        """ユーザー作成"""
        try:
            # バリデーション
            if not name.strip():
                raise ValueError("Name cannot be empty")
            
            if "@" not in email:
                raise ValueError("Invalid email format")
            
            # 重複チェック
            for user in self.users.values():
                if user.email == email:
                    raise ValueError(f"Email {email} already exists")
            
            # ユーザー作成
            user = User(
                id=self.next_id,
                name=name.strip(),
                email=email.lower(),
                created_at=datetime.now()
            )
            
            self.users[self.next_id] = user
            self.next_id += 1
            
            return user
            
        except ValueError as e:
            raise DatabaseError(f"Failed to create user: {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unexpected error creating user: {e}") from e
    
    def batch_create_users(self, user_data_list: List[Dict[str, str]]) -> List[User]:
        """複数ユーザーの一括作成（トランザクション処理）"""
        created_users = []
        
        try:
            self.begin_transaction()
            
            for user_data in user_data_list:
                try:
                    user = self.create_user(user_data["name"], user_data["email"])
                    created_users.append(user)
                    print(f"Created user: {user.name}")
                except DatabaseError as e:
                    print(f"Error creating user {user_data}: {e}")
                    raise  # 一つでも失敗したらトランザクション全体を失敗させる
            
            self.commit_transaction()
            return created_users
            
        except Exception as e:
            # エラーが発生した場合はロールバック
            try:
                self.rollback_transaction()
            except TransactionError:
                pass  # ロールバックエラーは無視
            
            raise DatabaseError(f"Batch user creation failed: {e}") from e

# =============================================================================
# 実践テスト
# =============================================================================

def test_config_manager():
    """設定ファイル管理のテスト"""
    print("=== ConfigManager Test ===")
    
    config_path = "test_config.json"
    manager = ConfigManager(config_path)
    
    # 設定ファイル作成
    test_config = {
        "app_name": "MyApp",
        "version": "1.0.0",
        "debug": True,
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    try:
        manager.save_config(test_config)
        print("✓ Config saved successfully")
        
        loaded_config = manager.load_config()
        print(f"✓ Config loaded: {loaded_config['app_name']}")
        
        # 設定値取得
        debug_mode = manager.get_setting("debug")
        print(f"✓ Debug mode: {debug_mode}")
        
        # 存在しない設定値（デフォルト値付き）
        timeout = manager.get_setting("timeout", 30)
        print(f"✓ Timeout (default): {timeout}")
        
        # 存在しない設定値（エラー）
        try:
            manager.get_setting("nonexistent")
        except KeyError as e:
            print(f"✓ Expected error for missing setting: {e}")
    
    except FileProcessingError as e:
        print(f"✗ File processing error: {e}")
    finally:
        # クリーンアップ
        if os.path.exists(config_path):
            os.remove(config_path)

def test_api_client():
    """APIクライアントのテスト"""
    print("\n=== APIClient Test ===")
    
    client = APIClient("https://api.example.com", max_retries=3)
    
    try:
        data = client.fetch_data("/users")
        print(f"✓ API call succeeded: {data}")
    except NetworkError as e:
        print(f"✗ API call failed: {e}")

def test_database_manager():
    """データベース管理のテスト"""
    print("\n=== DatabaseManager Test ===")
    
    db = DatabaseManager()
    
    # 正常なユーザー作成
    try:
        user1 = db.create_user("Alice", "alice@example.com")
        print(f"✓ Created user: {user1}")
        
        user2 = db.create_user("Bob", "bob@example.com")
        print(f"✓ Created user: {user2}")
    except DatabaseError as e:
        print(f"✗ User creation failed: {e}")
    
    # 一括作成（成功パターン）
    print("\n--- Batch creation (success) ---")
    user_data_success = [
        {"name": "Charlie", "email": "charlie@example.com"},
        {"name": "Diana", "email": "diana@example.com"}
    ]
    
    try:
        created_users = db.batch_create_users(user_data_success)
        print(f"✓ Batch creation succeeded: {len(created_users)} users created")
    except DatabaseError as e:
        print(f"✗ Batch creation failed: {e}")
    
    # 一括作成（失敗パターン - 重複メール）
    print("\n--- Batch creation (failure) ---")
    user_data_failure = [
        {"name": "Eve", "email": "eve@example.com"},
        {"name": "Frank", "email": "alice@example.com"},  # 重複
        {"name": "Grace", "email": "grace@example.com"}
    ]
    
    try:
        created_users = db.batch_create_users(user_data_failure)
        print(f"✓ Batch creation succeeded: {len(created_users)} users created")
    except DatabaseError as e:
        print(f"✓ Expected batch creation failure: {e}")
    
    print(f"\nFinal user count: {len(db.users)}")
    for user in db.users.values():
        print(f"  - {user.name} ({user.email})")

if __name__ == "__main__":
    test_config_manager()
    test_api_client()
    test_database_manager()
