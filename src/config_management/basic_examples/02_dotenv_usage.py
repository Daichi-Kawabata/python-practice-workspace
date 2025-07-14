"""
02_dotenv_usage.py - python-dotenv を使った設定管理

python-dotenv とは：
- .env ファイルから環境変数を読み込むライブラリ
- 開発時の設定管理が簡単になる
- プロダクションコードに設定を書かずに済む
"""

import os
from pathlib import Path
from typing import Optional

# python-dotenv をインストール: pip install python-dotenv
try:
    from dotenv import load_dotenv, find_dotenv, dotenv_values
    DOTENV_AVAILABLE = True
except ImportError:
    print("python-dotenv がインストールされていません")
    print("インストール: pip install python-dotenv")
    DOTENV_AVAILABLE = False


def create_sample_env_files():
    """サンプルの .env ファイルを作成"""

    print("=" * 50)
    print("サンプル .env ファイルの作成")
    print("=" * 50)

    # 基本的な .env ファイル
    env_content = """# アプリケーション設定
APP_NAME=My Python App
APP_VERSION=1.0.0
DEBUG=true

# データベース設定
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
DATABASE_POOL_SIZE=20

# API 設定
API_KEY=your-secret-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_EXPIRE_MINUTES=30

# Redis 設定
REDIS_URL=redis://localhost:6379/0

# ログ設定
LOG_LEVEL=DEBUG
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# 外部サービス設定
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-email-password

# その他
MAX_UPLOAD_SIZE=10485760
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
"""

    # .env ファイルを作成
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)

    print("✅ .env ファイルを作成しました")

    # 環境別の設定ファイル
    env_dev_content = """# 開発環境設定
APP_NAME=My Python App (Development)
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379/1
"""

    env_prod_content = """# 本番環境設定
APP_NAME=My Python App (Production)
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://prod_user:prod_pass@prod-server:5432/myapp_prod
REDIS_URL=redis://prod-redis:6379/0
"""

    with open(".env.development", "w", encoding="utf-8") as f:
        f.write(env_dev_content)

    with open(".env.production", "w", encoding="utf-8") as f:
        f.write(env_prod_content)

    print("✅ 環境別設定ファイルを作成しました")
    print("  - .env.development")
    print("  - .env.production")


def demonstrate_dotenv_usage():
    """python-dotenv の基本的な使用方法"""

    if not DOTENV_AVAILABLE:
        return

    print("\n" + "=" * 50)
    print("python-dotenv の基本使用方法")
    print("=" * 50)

    # 1. 基本的な .env ファイルの読み込み
    print("\n【1. .env ファイルの読み込み】")

    # .env ファイルを環境変数に読み込み
    load_dotenv()

    # 読み込まれた環境変数にアクセス
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    debug = os.getenv("DEBUG")

    print(f"アプリケーション名: {app_name}")
    print(f"バージョン: {app_version}")
    print(f"デバッグモード: {debug}")

    # 2. 特定の .env ファイルを指定して読み込み
    print("\n【2. 特定の .env ファイルの読み込み】")

    # 開発環境設定を読み込み
    load_dotenv(".env.development", override=True)

    app_name_dev = os.getenv("APP_NAME")
    debug_dev = os.getenv("DEBUG")
    db_url_dev = os.getenv("DATABASE_URL")

    print(f"開発環境 - アプリ名: {app_name_dev}")
    print(f"開発環境 - デバッグ: {debug_dev}")
    print(f"開発環境 - DB URL: {db_url_dev}")

    # 3. dotenv_values() で辞書として取得
    print("\n【3. 設定を辞書として取得】")

    # .env ファイルの内容を辞書として取得（環境変数には設定しない）
    config = dotenv_values(".env")

    print("設定値一覧:")
    for key, value in config.items():
        # 機密情報をマスク
        if any(secret_word in key.lower() for secret_word in ["password", "secret", "key"]):
            masked_value = "*" * len(value) if value else ""
            print(f"  {key}: {masked_value}")
        else:
            print(f"  {key}: {value}")


def advanced_dotenv_patterns():
    """高度な dotenv の使用パターン"""

    if not DOTENV_AVAILABLE:
        return

    print("\n" + "=" * 50)
    print("高度な dotenv 使用パターン")
    print("=" * 50)

    # 1. 自動的な .env ファイル検索
    print("\n【1. 自動 .env ファイル検索】")

    # 現在のディレクトリから上に向かって .env ファイルを検索
    dotenv_path = find_dotenv()
    print(f"発見された .env ファイル: {dotenv_path}")

    # 2. 階層的な設定の読み込み
    print("\n【2. 階層的な設定読み込み】")

    def load_config_hierarchically():
        """階層的に設定を読み込む"""

        # 1. デフォルト設定
        load_dotenv(".env")

        # 2. 環境固有設定（存在する場合）
        env = os.getenv("ENVIRONMENT", "development")
        env_file = f".env.{env}"

        if Path(env_file).exists():
            load_dotenv(env_file, override=True)
            print(f"✅ {env_file} を読み込みました")
        else:
            print(f"⚠️  {env_file} が見つかりません")

        # 3. ローカル設定（.env.local）- Git管理外
        if Path(".env.local").exists():
            load_dotenv(".env.local", override=True)
            print("✅ .env.local を読み込みました")

    load_config_hierarchically()

    # 3. 設定の検証
    print("\n【3. 設定値の検証】")

    def validate_config():
        """設定値の検証"""
        errors = []

        # 必須項目のチェック
        required_vars = ["APP_NAME", "DATABASE_URL", "JWT_SECRET_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                errors.append(f"必須環境変数 {var} が設定されていません")

        # 形式のチェック
        database_url = os.getenv("DATABASE_URL", "")
        if database_url and not database_url.startswith(("postgresql://", "sqlite:///")):
            errors.append("DATABASE_URL の形式が正しくありません")

        # 数値のチェック
        try:
            jwt_expire = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
            if jwt_expire <= 0:
                errors.append("JWT_EXPIRE_MINUTES は正の数である必要があります")
        except ValueError:
            errors.append("JWT_EXPIRE_MINUTES は数値である必要があります")

        if errors:
            print("❌ 設定エラー:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ 設定検証が成功しました")
            return True

    validate_config()


def config_class_pattern():
    """設定クラスパターンの実装"""

    print("\n" + "=" * 50)
    print("設定クラスパターン")
    print("=" * 50)

    class Config:
        """アプリケーション設定クラス"""

        def __init__(self):
            # .env ファイルを読み込み
            if DOTENV_AVAILABLE:
                load_dotenv()

            # 設定の読み込み
            self.APP_NAME = os.getenv("APP_NAME", "Default App")
            self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
            self.DEBUG = self._get_bool("DEBUG", False)

            # データベース設定
            self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
            self.DATABASE_POOL_SIZE = self._get_int("DATABASE_POOL_SIZE", 10)

            # API 設定
            self.API_KEY = os.getenv("API_KEY")
            self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret")
            self.JWT_EXPIRE_MINUTES = self._get_int("JWT_EXPIRE_MINUTES", 30)

            # Redis 設定
            self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

            # ログ設定
            self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

            # その他
            self.MAX_UPLOAD_SIZE = self._get_int(
                "MAX_UPLOAD_SIZE", 10485760)  # 10MB
            self.ALLOWED_HOSTS = self._get_list("ALLOWED_HOSTS", ["localhost"])
            self.CORS_ORIGINS = self._get_list(
                "CORS_ORIGINS", ["http://localhost:3000"])

        def _get_bool(self, key: str, default: bool = False) -> bool:
            """環境変数をブール値として取得"""
            value = os.getenv(key, "").lower()
            return value in ("true", "1", "yes", "on")

        def _get_int(self, key: str, default: int = 0) -> int:
            """環境変数を整数として取得"""
            try:
                return int(os.getenv(key, str(default)))
            except ValueError:
                return default

        def _get_list(self, key: str, default: Optional[list] = None) -> list:
            """環境変数をリストとして取得"""
            if default is None:
                default = []

            value = os.getenv(key, "")
            if not value:
                return default

            return [item.strip() for item in value.split(",")]

        def validate(self):
            """設定の検証"""
            if not self.JWT_SECRET_KEY:
                raise ValueError("JWT_SECRET_KEY は必須です")

            if self.JWT_EXPIRE_MINUTES <= 0:
                raise ValueError("JWT_EXPIRE_MINUTES は正の数である必要があります")

        def to_dict(self) -> dict:
            """設定を辞書として返す（機密情報はマスク）"""
            config_dict = {}
            for key, value in self.__dict__.items():
                if any(secret in key.lower() for secret in ["password", "secret", "key"]):
                    config_dict[key] = "*" * len(str(value)) if value else ""
                else:
                    config_dict[key] = value
            return config_dict

    # 使用例
    try:
        config = Config()
        config.validate()

        print("設定読み込み成功:")
        for key, value in config.to_dict().items():
            print(f"  {key}: {value}")

    except ValueError as e:
        print(f"❌ 設定エラー: {e}")


if __name__ == "__main__":
    # サンプル .env ファイルの作成
    create_sample_env_files()

    if DOTENV_AVAILABLE:
        # 基本的な使用方法
        demonstrate_dotenv_usage()

        # 高度なパターン
        advanced_dotenv_patterns()

        # 設定クラスパターン
        config_class_pattern()

    print("\n" + "=" * 50)
    print("まとめ")
    print("=" * 50)
    print("1. .env ファイルで開発時の設定管理が簡単に")
    print("2. 環境別設定ファイルで柔軟な設定管理")
    print("3. 設定クラスで型安全な設定管理")
    print("4. 検証機能で設定ミスを防止")
    print("5. 機密情報の適切な管理")
