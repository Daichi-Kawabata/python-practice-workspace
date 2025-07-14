#!/usr/bin/env python3
"""
環境変数を活用したPythonアプリケーション

Dockerコンテナでの環境変数管理のベストプラクティスを学習
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# ログ設定（環境変数から設定）
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """設定管理クラス - 環境変数からの設定読み込み"""

    def __init__(self):
        # 必須環境変数
        self.app_name = os.getenv('APP_NAME', 'Environment Demo App')
        self.app_version = os.getenv('APP_VERSION', '1.0.0')
        self.environment = os.getenv('ENVIRONMENT', 'development')

        # データベース設定
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', '5432'))
        self.db_name = os.getenv('DB_NAME', 'myapp')
        self.db_user = os.getenv('DB_USER', 'user')
        self.db_password = os.getenv('DB_PASSWORD', 'password')

        # Redis設定
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

        # API設定
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        self.external_api_url = os.getenv(
            'EXTERNAL_API_URL', 'https://api.example.com')

        # 機能フラグ
        self.debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
        self.enable_cache = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
        self.enable_metrics = os.getenv(
            'ENABLE_METRICS', 'false').lower() == 'true'

        # 数値設定
        self.max_connections = int(os.getenv('MAX_CONNECTIONS', '10'))
        self.timeout_seconds = float(os.getenv('TIMEOUT_SECONDS', '30.0'))

        # リスト形式の環境変数（カンマ区切り）
        allowed_hosts_str = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
        self.allowed_hosts = [host.strip()
                              for host in allowed_hosts_str.split(',')]

        # JSON形式の環境変数
        feature_flags_str = os.getenv('FEATURE_FLAGS', '{}')
        try:
            self.feature_flags = json.loads(feature_flags_str)
        except json.JSONDecodeError:
            logger.warning(
                "Invalid FEATURE_FLAGS JSON, using default empty dict")
            self.feature_flags = {}

    def get_database_url(self) -> str:
        """データベースURL生成"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def is_production(self) -> bool:
        """本番環境かどうか"""
        return self.environment.lower() == 'production'

    def is_development(self) -> bool:
        """開発環境かどうか"""
        return self.environment.lower() == 'development'

    def validate_config(self) -> Dict[str, Any]:
        """設定の検証"""
        issues = []

        # 必須設定の確認
        if not self.api_key and self.is_production():
            issues.append("API_KEY is required in production")

        if not self.api_secret and self.is_production():
            issues.append("API_SECRET is required in production")

        if self.max_connections <= 0:
            issues.append("MAX_CONNECTIONS must be positive")

        if self.timeout_seconds <= 0:
            issues.append("TIMEOUT_SECONDS must be positive")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    def to_dict(self, include_secrets: bool = False) -> Dict[str, Any]:
        """設定を辞書形式で返す"""
        config = {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment,
            "debug_mode": self.debug_mode,
            "enable_cache": self.enable_cache,
            "enable_metrics": self.enable_metrics,
            "max_connections": self.max_connections,
            "timeout_seconds": self.timeout_seconds,
            "allowed_hosts": self.allowed_hosts,
            "feature_flags": self.feature_flags,
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_name": self.db_name,
            "redis_url": self.redis_url,
            "external_api_url": self.external_api_url
        }

        if include_secrets:
            config.update({
                "db_user": self.db_user,
                "db_password": "***" if self.db_password else None,
                "api_key": "***" if self.api_key else None,
                "api_secret": "***" if self.api_secret else None
            })

        return config


def demonstrate_environment_usage():
    """環境変数使用例のデモ"""

    print("=" * 60)
    print("🌍 環境変数を活用したPythonアプリケーション")
    print("=" * 60)

    # 設定管理インスタンス作成
    config = ConfigManager()

    # 基本情報表示
    print(f"📱 アプリケーション: {config.app_name}")
    print(f"🔢 バージョン: {config.app_version}")
    print(f"🌍 環境: {config.environment}")
    print(f"🐛 デバッグモード: {config.debug_mode}")
    print(f"🕐 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")

    # 設定検証
    validation = config.validate_config()
    print(f"\n⚙️  設定検証: {'✅ 正常' if validation['valid'] else '❌ エラー'}")
    if validation['issues']:
        for issue in validation['issues']:
            print(f"  ⚠️  {issue}")

    # データベース設定
    print(f"\n💾 データベース設定:")
    if config.debug_mode:
        print(f"  URL: {config.get_database_url()}")
    else:
        print(f"  ホスト: {config.db_host}:{config.db_port}")
        print(f"  データベース名: {config.db_name}")

    # キャッシュ設定
    print(f"\n📦 キャッシュ設定:")
    print(f"  有効: {config.enable_cache}")
    if config.enable_cache:
        print(f"  Redis URL: {config.redis_url}")

    # API設定
    print(f"\n🔗 API設定:")
    print(f"  外部API URL: {config.external_api_url}")
    print(f"  APIキー設定: {'✅' if config.api_key else '❌'}")
    print(f"  API秘密鍵設定: {'✅' if config.api_secret else '❌'}")

    # ネットワーク設定
    print(f"\n🌐 ネットワーク設定:")
    print(f"  最大接続数: {config.max_connections}")
    print(f"  タイムアウト: {config.timeout_seconds}秒")
    print(f"  許可ホスト: {', '.join(config.allowed_hosts)}")

    # 機能フラグ
    print(f"\n🚩 機能フラグ:")
    print(f"  メトリクス有効: {config.enable_metrics}")
    if config.feature_flags:
        print("  カスタムフラグ:")
        for key, value in config.feature_flags.items():
            print(f"    {key}: {value}")
    else:
        print("  カスタムフラグ: なし")

    # 環境固有の処理
    print(f"\n🎯 環境固有の処理:")
    if config.is_production():
        print("  🚀 本番環境モード")
        print("    - 詳細ログ無効")
        print("    - セキュリティ強化")
        print("    - パフォーマンス最適化")
    elif config.is_development():
        print("  🛠️  開発環境モード")
        print("    - 詳細ログ有効")
        print("    - デバッグ機能有効")
        print("    - ホットリロード有効")
    else:
        print("  🧪 テスト/ステージング環境")
        print("    - 本番に準じた設定")
        print("    - テスト用データ使用")

    # 設定のエクスポート（デバッグモードの場合）
    if config.debug_mode:
        print(f"\n📋 完全な設定情報:")
        full_config = config.to_dict(include_secrets=True)
        for key, value in full_config.items():
            print(f"  {key}: {value}")


def main():
    """メイン関数"""
    logger.info("Starting environment configuration demo")

    try:
        demonstrate_environment_usage()
        print(f"\n✅ アプリケーション実行完了!")
        logger.info("Application completed successfully")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
