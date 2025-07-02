"""
Python例外処理学習
Ruby/Golangとの比較を含む実践的な例
try/except、カスタム例外、コンテキストマネージャーなど
"""

import sys
import logging
from typing import Generator, Optional, List, Union, Any
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

# =============================================================================
# 1. 基本的な例外処理
# =============================================================================

def basic_exception_handling():
    """
    基本的なtry/except構文
    Ruby: begin/rescue/end
    Go: if err != nil { return err }
    """
    
    # 基本形
    try:
        result = 10 / 0  # ZeroDivisionError が発生
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
    
    # 複数の例外をキャッチ
    try:
        numbers = [1, 2, 3]
        print(numbers[10])  # IndexError
        print(int("abc"))   # ValueError
    except IndexError:
        print("Index out of range!")
    except ValueError:
        print("Invalid value!")
    
    # 複数例外を一度にキャッチ
    try:
        # 何らかの処理
        data = {"key": "value"}
        result = data["missing_key"]  # KeyError
    except (KeyError, ValueError, TypeError) as e:
        print(f"Multiple exception caught: {e}")
    
    # すべての例外をキャッチ（推奨されない）
    try:
        risky_operation()
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # finally句（必ず実行される）
    try:
        file = open("nonexistent.txt")
    except FileNotFoundError:
        print("File not found")
    finally:
        print("Cleanup code here")  # 必ず実行される

def risky_operation():
    raise RuntimeError("Something went wrong")

# =============================================================================
# 2. 例外の詳細情報取得
# =============================================================================

def exception_details():
    """例外の詳細情報を取得する方法"""
    
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        # 例外オブジェクトの情報
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print(f"Exception args: {e.args}")
    
    # トレースバック情報
    import traceback
    
    try:
        nested_function_call()
    except Exception as e:
        print("=== Traceback Information ===")
        print(f"Exception: {e}")
        traceback.print_exc()  # スタックトレースを出力

def nested_function_call():
    def level1():
        def level2():
            def level3():
                raise ValueError("Deep error")
            level3()
        level2()
    level1()

# =============================================================================
# 3. カスタム例外クラス
# =============================================================================

class CustomError(Exception):
    """
    基本的なカスタム例外
    Ruby: class CustomError < StandardError; end
    Go: type CustomError struct { message string }
    """
    pass

class ValidationError(Exception):
    """バリデーションエラー"""
    
    def __init__(self, field: str, value: Any, message: str = "") -> None:
        self.field = field
        self.value = value
        self.message = message or f"Invalid value for {field}: {value}"
        super().__init__(self.message)

class BusinessLogicError(Exception):
    """ビジネスロジックエラー"""
    
    def __init__(self, code: str, message: str, details: Optional[dict] = None) -> None:
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{code}] {message}")

class InsufficientFundsError(BusinessLogicError):
    """残高不足エラー"""
    
    def __init__(self, requested: float, available: float) -> None:
        super().__init__(
            code="INSUFFICIENT_FUNDS",
            message=f"Requested ${requested}, but only ${available} available",
            details={"requested": requested, "available": available}
        )

# =============================================================================
# 4. 例外の再発生（re-raise）
# =============================================================================

def exception_reraising():
    """例外の再発生パターン"""
    
    # パターン1: ログ出力後に再発生
    try:
        dangerous_operation()
    except Exception as e:
        logging.error(f"Error in dangerous_operation: {e}")
        raise  # 元の例外を再発生
    
    # パターン2: 例外を変換して再発生
    try:
        external_api_call()
    except ConnectionError as e:
        # 外部ライブラリの例外を自分の例外に変換
        raise BusinessLogicError("API_ERROR", "Failed to connect to external service") from e
    
    # パターン3: 追加情報を付与して再発生
    try:
        process_user_data({"invalid": "data"})
    except KeyError as e:
        raise ValidationError("user_data", "missing_field", f"Required field missing: {e}") from e

def dangerous_operation():
    raise RuntimeError("Simulated error")

def external_api_call():
    raise ConnectionError("Network timeout")

def process_user_data(data: dict):
    return data["required_field"]  # KeyError if missing

# =============================================================================
# 5. else句とfinally句の活用
# =============================================================================

def else_finally_examples():
    """else句とfinally句の使い分け"""
    
    # else句: 例外が発生しなかった場合のみ実行
    try:
        result = 10 / 2
    except ZeroDivisionError:
        print("Division by zero")
    else:
        print(f"Division successful: {result}")  # 例外がなかった場合のみ
    finally:
        print("Cleanup")  # 必ず実行
    
    # ファイル処理の例
    filename = "example.txt"
    file = None
    
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print(f"File {filename} not found")
    else:
        # ファイルが正常に開けた場合のみ読み込み
        content = file.read()
        print(f"File content: {content}")
    finally:
        # ファイルが開けていれば必ずクローズ
        if file and not file.closed:
            file.close()
            print("File closed")

# =============================================================================
# 6. コンテキストマネージャー（with文）
# =============================================================================

def context_manager_examples():
    """
    コンテキストマネージャーの使用
    Ruby: begin/ensure/end に近い
    Go: defer文に近い
    """
    
    # ファイル処理（自動クローズ）
    try:
        with open("example.txt", "w") as file:
            file.write("Hello, World!")
            # ファイルは自動的にクローズされる
    except IOError as e:
        print(f"File I/O error: {e}")
    
    # 複数リソースの管理
    try:
        with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
            data = infile.read()
            outfile.write(data.upper())
    except FileNotFoundError:
        print("Input file not found")

# カスタムコンテキストマネージャー
class DatabaseConnection:
    """データベース接続のコンテキストマネージャー例"""
    
    def __init__(self, connection_string: str) -> None:
        self.connection_string: str = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.connection_string}")
        self.connection: Optional[str] = f"Connection to {self.connection_string}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print("Closing database connection")
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
            # False を返すと例外が再発生される
            return False
        return True

@contextmanager
def timer_context() -> Generator[float, Any, None]:
    """関数ベースのコンテキストマネージャー"""
    import time
    start_time = time.time()
    print("Timer started")
    try:
        yield start_time
    finally:
        end_time = time.time()
        print(f"Timer finished: {end_time - start_time:.2f} seconds")

# =============================================================================
# 7. 実践的な例外処理パターン
# =============================================================================

@dataclass
class User:
    id: int
    name: str
    email: str
    age: int

class UserService:
    """実践的な例外処理を含むユーザーサービス"""
    
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
    
    def create_user(self, name: str, email: str, age: int) -> User:
        """ユーザー作成（バリデーション付き）"""
        try:
            # バリデーション
            self._validate_user_data(name, email, age)
            
            # ユーザーID生成
            user_id = len(self.users) + 1
            
            # ユーザー作成
            user = User(user_id, name, email, age)
            self.users[user_id] = user
            
            return user
            
        except ValidationError:
            # バリデーションエラーはそのまま再発生
            raise
        except Exception as e:
            # 予期しないエラーをビジネス例外に変換
            raise BusinessLogicError(
                "USER_CREATION_FAILED",
                "Failed to create user due to system error"
            ) from e
    
    def _validate_user_data(self, name: str, email: str, age: int) -> None:
        """ユーザーデータのバリデーション"""
        if not name or len(name.strip()) == 0:
            raise ValidationError("name", name, "Name cannot be empty")
        
        if not email or "@" not in email:
            raise ValidationError("email", email, "Invalid email format")
        
        if age < 0 or age > 150:
            raise ValidationError("age", age, "Age must be between 0 and 150")
    
    def get_user(self, user_id: int) -> User:
        """ユーザー取得"""
        try:
            return self.users[user_id]
        except KeyError:
            raise BusinessLogicError(
                "USER_NOT_FOUND",
                f"User with ID {user_id} not found"
            )
    
    def update_user_email(self, user_id: int, new_email: str) -> User:
        """ユーザーのメールアドレス更新"""
        try:
            user = self.get_user(user_id)  # BusinessLogicError の可能性
            
            # メールアドレスのバリデーション
            if not new_email or "@" not in new_email:
                raise ValidationError("email", new_email, "Invalid email format")
            
            user.email = new_email
            return user
            
        except (ValidationError, BusinessLogicError):
            # 既知の例外はそのまま再発生
            raise
        except Exception as e:
            raise BusinessLogicError(
                "UPDATE_FAILED",
                "Failed to update user email"
            ) from e

# =============================================================================
# 8. ログ機能と例外処理の組み合わせ
# =============================================================================

def setup_logging():
    """ログ設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class BankAccount:
    """ログ機能付きの銀行口座クラス"""
    
    def __init__(self, account_number: str, initial_balance: float = 0.0) -> None:
        self.account_number = account_number
        self.balance = initial_balance
        self.logger = logging.getLogger(f"BankAccount.{account_number}")
    
    def deposit(self, amount: float) -> None:
        """入金処理"""
        try:
            if amount <= 0:
                raise ValidationError("amount", amount, "Deposit amount must be positive")
            
            self.balance += amount
            self.logger.info(f"Deposited ${amount}. New balance: ${self.balance}")
            
        except ValidationError as e:
            self.logger.error(f"Deposit failed: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error during deposit: {e}")
            raise BusinessLogicError("DEPOSIT_FAILED", "System error during deposit") from e
    
    def withdraw(self, amount: float) -> None:
        """出金処理"""
        try:
            if amount <= 0:
                raise ValidationError("amount", amount, "Withdrawal amount must be positive")
            
            if self.balance < amount:
                raise InsufficientFundsError(amount, self.balance)
            
            self.balance -= amount
            self.logger.info(f"Withdrew ${amount}. New balance: ${self.balance}")
            
        except (ValidationError, InsufficientFundsError) as e:
            self.logger.warning(f"Withdrawal failed: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error during withdrawal: {e}")
            raise BusinessLogicError("WITHDRAWAL_FAILED", "System error during withdrawal") from e

# =============================================================================
# 使用例・テスト
# =============================================================================

if __name__ == "__main__":
    setup_logging()
    
    print("=== 基本的な例外処理 ===")
    basic_exception_handling()
    
    print("\n=== 例外詳細情報 ===")
    exception_details()
    
    print("\n=== カスタム例外 ===")
    try:
        raise ValidationError("username", "", "Username cannot be empty")
    except ValidationError as e:
        print(f"Validation error: {e}")
        print(f"Field: {e.field}, Value: '{e.value}'")
    
    print("\n=== ビジネスロジック例外 ===")
    try:
        raise InsufficientFundsError(100.0, 50.0)
    except InsufficientFundsError as e:
        print(f"Business error: {e}")
        print(f"Details: {e.details}")
    
    print("\n=== コンテキストマネージャー ===")
    # データベース接続例
    try:
        with DatabaseConnection("postgresql://localhost:5432/mydb") as conn:
            print(f"Using connection: {conn}")
            # raise Exception("Database error")  # コメントアウトして試してみる
    except Exception as e:
        print(f"Database operation failed: {e}")
    
    # タイマー例
    with timer_context() as start_time:
        import time
        time.sleep(1)  # 1秒待機
        print(f"Started at: {start_time}")
    
    print("\n=== 実践的なユーザーサービス ===")
    user_service = UserService()
    
    try:
        # 正常なユーザー作成
        user1 = user_service.create_user("Alice", "alice@example.com", 25)
        print(f"Created user: {user1}")
        
        # バリデーションエラー
        user2 = user_service.create_user("", "invalid-email", -5)
    except ValidationError as e:
        print(f"Validation error: {e}")
    
    try:
        # 存在しないユーザーの取得
        user = user_service.get_user(999)
    except BusinessLogicError as e:
        print(f"Business error: {e.code} - {e.message}")
    
    print("\n=== 銀行口座例 ===")
    account = BankAccount("ACC001", 100.0)
    
    try:
        account.deposit(50.0)
        account.withdraw(200.0)  # 残高不足エラー
    except InsufficientFundsError as e:
        print(f"Insufficient funds: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except BusinessLogicError as e:
        print(f"Business error: {e}")
    
    print(f"Final balance: ${account.balance}")
