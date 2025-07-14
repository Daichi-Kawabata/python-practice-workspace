"""
FastAPI アプリケーションの設定管理

このファイルは実際のFastAPIアプリケーションで使用される
設定管理のベストプラクティスを示します。
"""

import os
import secrets
from typing import List, Optional
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """データベース設定"""

    # 開発環境用のデフォルト値
    url: str = Field(
        default="sqlite:///./app.db",
        description="データベース接続URL"
    )

    pool_size: int = Field(
        default=5,
        ge=1,
        le=50,
        description="データベース接続プール数"
    )

    echo: bool = Field(
        default=False,
        description="SQLクエリを出力するかどうか"
    )

    model_config = SettingsConfigDict(env_prefix="DB_", extra="ignore")


class RedisSettings(BaseSettings):
    """Redis設定"""

    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis接続URL"
    )

    max_connections: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Redis最大接続数"
    )

    model_config = SettingsConfigDict(env_prefix="REDIS_", extra="ignore")


class SecuritySettings(BaseSettings):
    """セキュリティ設定"""

    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="アプリケーションの秘密鍵"
    )

    jwt_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT署名用の秘密鍵"
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT署名アルゴリズム"
    )

    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        le=1440,  # 24時間
        description="アクセストークンの有効期限（分）"
    )

    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="許可するホスト"
    )

    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        description="CORS許可オリジン"
    )

    model_config = SettingsConfigDict(env_prefix="SECURITY_", extra="ignore")


class AppSettings(BaseSettings):
    """アプリケーション設定"""

    name: str = Field(
        default="FastAPI App",
        description="アプリケーション名"
    )

    version: str = Field(
        default="1.0.0",
        description="アプリケーションバージョン"
    )

    debug: bool = Field(
        default=False,
        description="デバッグモード"
    )

    environment: str = Field(
        default="development",
        description="実行環境"
    )

    log_level: str = Field(
        default="INFO",
        description="ログレベル"
    )

    # ネストした設定
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        """環境名のバリデーション"""
        allowed_environments = ['development', 'staging', 'production']
        if v not in allowed_environments:
            raise ValueError(
                f'Environment must be one of {allowed_environments}')
        return v

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        """ログレベルのバリデーション"""
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in allowed_levels:
            raise ValueError(f'Log level must be one of {allowed_levels}')
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# グローバル設定インスタンス
settings = AppSettings()


def get_settings() -> AppSettings:
    """設定を取得する関数（依存性注入用）"""
    return settings


def reload_settings():
    """設定を再読み込みする（テスト用）"""
    global settings
    settings = AppSettings()
    return settings


# 環境別設定ファクトリー
def create_settings_for_environment(env: str) -> AppSettings:
    """環境に応じた設定を作成"""
    env_file = f".env.{env}"

    # 環境ファイルが存在する場合のみ読み込み
    if os.path.exists(env_file):
        # 環境変数でenv_fileを指定
        old_env_file = os.environ.get('PYDANTIC_ENV_FILE')
        os.environ['PYDANTIC_ENV_FILE'] = env_file
        try:
            settings = AppSettings()
        finally:
            # 元の設定を復元
            if old_env_file:
                os.environ['PYDANTIC_ENV_FILE'] = old_env_file
            else:
                os.environ.pop('PYDANTIC_ENV_FILE', None)
        return settings
    else:
        # 環境変数から設定を作成
        os.environ.setdefault("ENVIRONMENT", env)
        return AppSettings()


# 設定表示用のヘルパー関数
def display_settings(settings: AppSettings, hide_secrets: bool = True):
    """設定内容を表示（機密情報は隠す）"""
    print("=" * 60)
    print("アプリケーション設定")
    print("=" * 60)

    print(f"📱 アプリケーション名: {settings.name}")
    print(f"🔢 バージョン: {settings.version}")
    print(f"🌍 環境: {settings.environment}")
    print(f"🐛 デバッグ: {settings.debug}")
    print(f"📊 ログレベル: {settings.log_level}")

    print("\n" + "=" * 60)
    print("データベース設定")
    print("=" * 60)

    db_url = settings.database.url
    if hide_secrets and "://" in db_url:
        # パスワード部分を隠す
        scheme, rest = db_url.split("://", 1)
        if "@" in rest:
            auth, host = rest.split("@", 1)
            if ":" in auth:
                user, _ = auth.split(":", 1)
                db_url = f"{scheme}://{user}:***@{host}"

    print(f"🗄️  データベースURL: {db_url}")
    print(f"🔗 プール数: {settings.database.pool_size}")
    print(f"👁️  SQLエコー: {settings.database.echo}")

    print("\n" + "=" * 60)
    print("Redis設定")
    print("=" * 60)

    print(f"🔴 RedisURL: {settings.redis.url}")
    print(f"🔗 最大接続数: {settings.redis.max_connections}")

    print("\n" + "=" * 60)
    print("セキュリティ設定")
    print("=" * 60)

    secret_key = settings.security.secret_key
    jwt_secret = settings.security.jwt_secret_key

    if hide_secrets:
        secret_key = f"{secret_key[:8]}***{secret_key[-8:]}"
        jwt_secret = f"{jwt_secret[:8]}***{jwt_secret[-8:]}"

    print(f"🔐 秘密鍵: {secret_key}")
    print(f"🎫 JWT秘密鍵: {jwt_secret}")
    print(f"🔑 JWTアルゴリズム: {settings.security.jwt_algorithm}")
    print(f"⏰ トークン有効期限: {settings.security.access_token_expire_minutes}分")
    print(f"🏠 許可ホスト: {settings.security.allowed_hosts}")
    print(f"🌐 CORS許可オリジン: {settings.security.cors_origins}")


if __name__ == "__main__":
    # デモンストレーション
    print("FastAPI設定管理のデモンストレーション")

    # 基本設定の表示
    display_settings(settings)

    # 環境別設定のテスト
    print("\n" + "=" * 60)
    print("環境別設定のテスト")
    print("=" * 60)

    for env in ['development', 'staging', 'production']:
        print(f"\n【{env.upper()}環境】")
        env_settings = create_settings_for_environment(env)
        print(f"環境: {env_settings.environment}")
        print(f"デバッグ: {env_settings.debug}")
        print(f"ログレベル: {env_settings.log_level}")
