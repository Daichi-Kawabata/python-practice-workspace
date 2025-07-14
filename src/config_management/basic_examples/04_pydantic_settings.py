"""
04_pydantic_settings.py - Pydantic Settings を使った型安全な設定管理

Pydantic Settings とは：
- Pydantic をベースにした設定管理ライブラリ
- 型安全な設定管理
- 自動的なバリデーション
- 環境変数、.env ファイル、JSON ファイルなど複数のソースから設定を読み込み
"""

import os
from pathlib import Path
from typing import List, Optional

# 必要なパッケージをインストール: pip install pydantic pydantic-settings
try:
    from pydantic import Field, field_validator
    from pydantic_settings import BaseSettings, SettingsConfigDict
    PYDANTIC_AVAILABLE = True
except ImportError:
    print("Pydantic がインストールされていません")
    print("インストール: pip install pydantic pydantic-settings")
    PYDANTIC_AVAILABLE = False


if PYDANTIC_AVAILABLE:

    class DatabaseSettings(BaseSettings):
        """データベース設定"""

        database_url: str = Field(
            default="sqlite:///./app.db",
            description="データベース接続URL"
        )
        database_pool_size: int = Field(
            default=10,
            ge=1,
            le=100,
            description="データベース接続プールサイズ"
        )
        database_timeout: int = Field(
            default=30,
            ge=1,
            description="データベース接続タイムアウト（秒）"
        )

        @field_validator('database_url')
        @classmethod
        def validate_database_url(cls, v):
            """データベースURLの検証"""
            allowed_schemes = ['postgresql', 'mysql', 'sqlite']
            if not any(v.startswith(f'{scheme}://') for scheme in allowed_schemes):
                raise ValueError(
                    f'データベースURLのスキームは {allowed_schemes} のいずれかである必要があります')
            return v

        model_config = SettingsConfigDict(env_prefix="DB_")

    class RedisSettings(BaseSettings):
        """Redis設定"""

        redis_url: str = Field(
            default="redis://localhost:6379/0",
            description="Redis接続URL"
        )
        redis_password: Optional[str] = Field(
            default=None,
            description="Redisパスワード"
        )
        redis_max_connections: int = Field(
            default=20,
            ge=1,
            description="Redis最大接続数"
        )

        model_config = SettingsConfigDict(env_prefix="REDIS_")

    class AuthSettings(BaseSettings):
        """認証設定"""

        jwt_secret_key: str = Field(
            ...,  # 必須項目
            min_length=32,
            description="JWT署名用秘密鍵"
        )
        jwt_algorithm: str = Field(
            default="HS256",
            description="JWT署名アルゴリズム"
        )
        jwt_expire_minutes: int = Field(
            default=30,
            ge=1,
            le=10080,  # 1週間
            description="JWTトークン有効期限（分）"
        )

        model_config = SettingsConfigDict(env_prefix="AUTH_")

    class LoggingSettings(BaseSettings):
        """ログ設定"""

        log_level: str = Field(
            default="INFO",
            description="ログレベル"
        )
        log_format: str = Field(
            default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            description="ログフォーマット"
        )
        log_file: Optional[str] = Field(
            default=None,
            description="ログファイルパス"
        )

        @field_validator('log_level')
        @classmethod
        def validate_log_level(cls, v):
            """ログレベルの検証"""
            allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            v_upper = v.upper()
            if v_upper not in allowed_levels:
                raise ValueError(f'ログレベルは {allowed_levels} のいずれかである必要があります')
            return v_upper

        model_config = SettingsConfigDict(env_prefix="LOG_")

    class AppSettings(BaseSettings):
        """メインアプリケーション設定"""

        # 基本設定
        app_name: str = Field(
            default="My Python App",
            description="アプリケーション名"
        )
        app_version: str = Field(
            default="1.0.0",
            description="アプリケーションバージョン"
        )
        debug: bool = Field(
            default=False,
            description="デバッグモード"
        )
        environment: str = Field(
            default="production",
            description="実行環境"
        )

        # サーバー設定
        host: str = Field(
            default="127.0.0.1",
            description="バインドホスト"
        )
        port: int = Field(
            default=8000,
            ge=1,
            le=65535,
            description="バインドポート"
        )

        # セキュリティ設定
        allowed_hosts: List[str] = Field(
            default=["localhost", "127.0.0.1"],
            description="許可ホスト一覧"
        )
        cors_origins: List[str] = Field(
            default=["http://localhost:3000"],
            description="CORS許可オリジン一覧"
        )

        # ファイルアップロード設定
        max_upload_size: int = Field(
            default=10485760,  # 10MB
            ge=1,
            description="最大アップロードサイズ（バイト）"
        )

        # 外部設定の組み込み
        database: DatabaseSettings = Field(default_factory=DatabaseSettings)
        redis: RedisSettings = Field(default_factory=RedisSettings)
        auth: AuthSettings = Field(default_factory=lambda: AuthSettings(
            jwt_secret_key="change-me-in-production"))
        logging: LoggingSettings = Field(default_factory=LoggingSettings)

        @field_validator('environment')
        @classmethod
        def validate_environment(cls, v):
            """環境の検証"""
            allowed_envs = ['development', 'staging', 'production']
            if v not in allowed_envs:
                raise ValueError(f'環境は {allowed_envs} のいずれかである必要があります')
            return v

        @field_validator('allowed_hosts', mode='before')
        @classmethod
        def validate_allowed_hosts(cls, v):
            """許可ホストの検証"""
            if isinstance(v, str):
                # カンマ区切りの文字列を分割
                hosts = [host.strip() for host in v.split(',') if host.strip()]
                if not hosts:
                    raise ValueError('少なくとも1つの許可ホストが必要です')
                return hosts
            if isinstance(v, list):
                if not v:
                    raise ValueError('少なくとも1つの許可ホストが必要です')
                return v
            return v

        @field_validator('cors_origins', mode='before')
        @classmethod
        def validate_cors_origins(cls, v):
            """CORS オリジンの検証"""
            if isinstance(v, str):
                # カンマ区切りの文字列を分割
                return [origin.strip() for origin in v.split(',') if origin.strip()]
            return v

        model_config = SettingsConfigDict(
            env_file=".env",
            env_nested_delimiter="__",
            case_sensitive=False,
            env_parse_none_str="null"
        )


def demonstrate_pydantic_settings():
    """Pydantic Settings の基本的な使用方法"""

    if not PYDANTIC_AVAILABLE:
        return

    print("=" * 50)
    print("Pydantic Settings の基本使用方法")
    print("=" * 50)

    # 1. 環境変数を設定
    os.environ.update({
        "APP_NAME": "Demo Application",
        "APP_VERSION": "2.0.0",
        "DEBUG": "true",
        "ENVIRONMENT": "development",
        "PORT": "8080",
        "DB__DATABASE_URL": "postgresql://localhost/demo",
        "DB__DATABASE_POOL_SIZE": "15",
        "AUTH__JWT_SECRET_KEY": "super-secret-key-for-demo-purposes-only",
        "AUTH__JWT_EXPIRE_MINUTES": "60",
        "LOG__LOG_LEVEL": "DEBUG",
        "ALLOWED_HOSTS": '["localhost", "127.0.0.1", "example.com"]',
        "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8080"]'
    })

    try:
        # 設定を読み込み
        settings = AppSettings()

        print("✅ 設定読み込み成功:")
        print(f"  アプリ名: {settings.app_name}")
        print(f"  バージョン: {settings.app_version}")
        print(f"  デバッグ: {settings.debug}")
        print(f"  環境: {settings.environment}")
        print(f"  ポート: {settings.port}")
        print(f"  DB URL: {settings.database.database_url}")
        print(f"  DB プールサイズ: {settings.database.database_pool_size}")
        print(f"  JWT有効期限: {settings.auth.jwt_expire_minutes}分")
        print(f"  ログレベル: {settings.logging.log_level}")
        print(f"  許可ホスト: {settings.allowed_hosts}")

    except Exception as e:
        print(f"❌ 設定エラー: {e}")


def demonstrate_validation_errors():
    """バリデーションエラーのデモ"""

    if not PYDANTIC_AVAILABLE:
        return

    print("\n" + "=" * 50)
    print("バリデーションエラーのデモ")
    print("=" * 50)

    # 不正な設定値を設定
    os.environ.update({
        "ENVIRONMENT": "invalid_env",
        "PORT": "99999",  # 範囲外
        "DB__DATABASE_URL": "invalid://url",
        "LOG__LOG_LEVEL": "INVALID_LEVEL",
        "AUTH__JWT_SECRET_KEY": "short",  # 短すぎる
        "AUTH__JWT_EXPIRE_MINUTES": "-1"  # 負の値
    })

    try:
        settings = AppSettings()
        print("❌ 予期しない成功")
    except Exception as e:
        print("✅ 期待通りバリデーションエラー:")
        print(f"  エラー詳細: {e}")


def demonstrate_environment_specific_config():
    """環境固有設定のデモ"""

    if not PYDANTIC_AVAILABLE:
        return

    print("\n" + "=" * 50)
    print("環境固有設定のデモ")
    print("=" * 50)

    class EnvironmentSpecificSettings(BaseSettings):
        """環境固有設定"""

        app_name: str = "Default App"
        debug: bool = False
        database_url: str = "sqlite:///./app.db"
        log_level: str = "INFO"

        model_config = SettingsConfigDict(
            case_sensitive=False
        )

        def __init__(self, **kwargs):
            # 環境に応じて異なる .env ファイルを読み込み
            env = os.getenv("ENVIRONMENT", "development")
            env_file = f".env.{env}"

            if Path(env_file).exists():
                print(f"✅ {env_file} を使用")
                # 環境固有のファイルを読み込み
                from dotenv import load_dotenv
                load_dotenv(env_file, override=True)
            else:
                print(f"⚠️  {env_file} が見つかりません")

            super().__init__(**kwargs)

    # 各環境での設定例
    environments = ["development", "staging", "production"]

    for env in environments:
        os.environ["ENVIRONMENT"] = env
        try:
            settings = EnvironmentSpecificSettings()
            print(f"\n{env.upper()} 環境:")
            print(f"  デバッグ: {settings.debug}")
            print(f"  ログレベル: {settings.log_level}")
        except Exception as e:
            print(f"❌ {env} 環境エラー: {e}")


def demonstrate_settings_export():
    """設定のエクスポート機能"""

    if not PYDANTIC_AVAILABLE:
        return

    print("\n" + "=" * 50)
    print("設定のエクスポート")
    print("=" * 50)

    # 不正な環境変数をクリア
    invalid_vars = ["ENVIRONMENT", "PORT", "DB__DATABASE_URL", "LOG__LOG_LEVEL",
                    "AUTH__JWT_SECRET_KEY", "AUTH__JWT_EXPIRE_MINUTES"]
    for var in invalid_vars:
        if var in os.environ:
            del os.environ[var]

    # クリーンな環境変数で設定
    clean_env = {
        "APP_NAME": "Export Demo",
        "DEBUG": "false",
        "ENVIRONMENT": "production",
        "PORT": "8000",
        "DB__DATABASE_URL": "postgresql://localhost/export_demo",
        "AUTH__JWT_SECRET_KEY": "export-demo-secret-key-for-testing",
        "ALLOWED_HOSTS": '["localhost", "127.0.0.1"]',
        "CORS_ORIGINS": '["http://localhost:3000"]'
    }

    for key, value in clean_env.items():
        os.environ[key] = value

    try:
        settings = AppSettings()

        # JSON として出力
        print("設定のJSON出力:")
        json_output = settings.model_dump_json(
            indent=2, exclude={"auth": {"jwt_secret_key"}})
        print(json_output)

        # 辞書として出力
        print("\n設定の辞書出力（機密情報除外）:")
        dict_output = settings.model_dump(exclude={"auth": {"jwt_secret_key"}})
        for key, value in dict_output.items():
            print(f"  {key}: {value}")

    except Exception as e:
        print(f"❌ エラー: {e}")


if __name__ == "__main__":
    if PYDANTIC_AVAILABLE:
        # 基本使用方法
        demonstrate_pydantic_settings()

        # バリデーションエラー
        demonstrate_validation_errors()

        # 環境固有設定
        demonstrate_environment_specific_config()

        # 設定エクスポート
        demonstrate_settings_export()

    print("\n" + "=" * 50)
    print("Pydantic Settings の利点")
    print("=" * 50)
    print("1. 型安全な設定管理")
    print("2. 自動的なバリデーション")
    print("3. ネストした設定構造")
    print("4. 複数のデータソース対応")
    print("5. IDE サポート（自動補完・型チェック）")
    print("6. 設定の文書化（Field の description）")
