"""
01_os_environ.py - 基本的な環境変数の使用方法

環境変数とは：
- オペレーティングシステムが管理する変数
- プログラムの実行時に外部から設定を渡すメカニズム
- 機密情報（パスワード、API キー）をコードに書かずに済む
"""

import os
from typing import Optional


def demonstrate_os_environ():
    """os.environ の基本的な使用方法を実演"""

    print("=" * 50)
    print("環境変数の基本操作")
    print("=" * 50)

    # 1. 環境変数の取得
    print("\n【1. 環境変数の取得】")

    # 方法1: os.environ[] - 存在しない場合は KeyError
    try:
        user = os.environ["USERNAME"]  # Windows の場合
        print(f"ユーザー名: {user}")
    except KeyError:
        try:
            user = os.environ["USER"]  # Unix/Linux の場合
            print(f"ユーザー名: {user}")
        except KeyError:
            print("ユーザー名が取得できませんでした")

    # 方法2: os.environ.get() - 存在しない場合はデフォルト値
    home = os.environ.get("HOME", "C:\\Users\\Default")
    print(f"ホームディレクトリ: {home}")

    # 方法3: os.getenv() - os.environ.get() のエイリアス
    path = os.getenv("PATH", "")
    print(f"PATH環境変数の文字数: {len(path)}")

    # 2. カスタム環境変数の設定と取得
    print("\n【2. カスタム環境変数の設定】")

    # 環境変数の設定
    os.environ["MY_APP_NAME"] = "Python Config Demo"
    os.environ["MY_APP_VERSION"] = "1.0.0"
    os.environ["DEBUG_MODE"] = "true"

    # 設定した環境変数の取得
    app_name = os.environ.get("MY_APP_NAME")
    app_version = os.environ.get("MY_APP_VERSION")
    debug_mode = os.environ.get("DEBUG_MODE")

    print(f"アプリケーション名: {app_name}")
    print(f"バージョン: {app_version}")
    print(f"デバッグモード: {debug_mode}")

    # 3. 型変換の必要性
    print("\n【3. 型変換の重要性】")

    # 環境変数は常に文字列として保存される
    print(f"DEBUG_MODE の型: {type(debug_mode)}")
    print(f"DEBUG_MODE の値: '{debug_mode}'")

    # ブール値への変換
    is_debug = debug_mode and debug_mode.lower() in ("true", "1", "yes", "on")
    print(f"ブール値に変換: {is_debug} (型: {type(is_debug)})")

    # 数値への変換
    os.environ["MAX_CONNECTIONS"] = "100"
    max_connections_str = os.environ.get("MAX_CONNECTIONS", "10")
    max_connections_int = int(max_connections_str)
    print(f"数値変換: '{max_connections_str}' → {max_connections_int}")


def safe_env_access():
    """安全な環境変数アクセスのパターン"""

    print("\n" + "=" * 50)
    print("安全な環境変数アクセスパターン")
    print("=" * 50)

    def get_env_as_bool(key: str, default: bool = False) -> bool:
        """環境変数をブール値として取得"""
        value = os.getenv(key, "").lower()
        return value in ("true", "1", "yes", "on")

    def get_env_as_int(key: str, default: int = 0) -> int:
        """環境変数を整数として取得"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default

    def get_env_as_list(key: str, separator: str = ",", default: Optional[list] = None) -> list:
        """環境変数をリストとして取得"""
        if default is None:
            default = []

        value = os.getenv(key, "")
        if not value:
            return default

        return [item.strip() for item in value.split(separator)]

    # 使用例
    os.environ["ENABLE_LOGGING"] = "true"
    os.environ["PORT"] = "8080"
    os.environ["ALLOWED_HOSTS"] = "localhost,127.0.0.1,example.com"

    enable_logging = get_env_as_bool("ENABLE_LOGGING")
    port = get_env_as_int("PORT", 3000)
    allowed_hosts = get_env_as_list("ALLOWED_HOSTS")

    print(f"ログ有効: {enable_logging}")
    print(f"ポート番号: {port}")
    print(f"許可ホスト: {allowed_hosts}")


def environment_variable_best_practices():
    """環境変数のベストプラクティス"""

    print("\n" + "=" * 50)
    print("環境変数のベストプラクティス")
    print("=" * 50)

    # 1. 命名規則
    print("\n【1. 命名規則】")
    print("✅ 良い例:")
    print("  - DATABASE_URL")
    print("  - JWT_SECRET_KEY")
    print("  - LOG_LEVEL")
    print("  - MAX_CONNECTIONS")

    print("\n❌ 悪い例:")
    print("  - dbUrl (大文字小文字混在)")
    print("  - secret (曖昧)")
    print("  - loglevel (アンダースコアなし)")

    # 2. 機密情報の管理
    print("\n【2. 機密情報の管理】")

    # 機密情報をコードにハードコーディングしない
    print("❌ 悪い例 (ハードコーディング):")
    print('DATABASE_URL = "postgresql://user:password@localhost/mydb"')

    print("\n✅ 良い例 (環境変数):")
    print('DATABASE_URL = os.getenv("DATABASE_URL")')

    # 3. デフォルト値の設定
    print("\n【3. デフォルト値の適切な設定】")

    # 本番環境で安全なデフォルト値
    log_level = os.getenv("LOG_LEVEL", "INFO")  # 本番では INFO
    debug_mode = get_env_as_bool("DEBUG", False)  # 本番では False

    print(f"ログレベル: {log_level}")
    print(f"デバッグモード: {debug_mode}")

    # 4. 必須環境変数のチェック
    print("\n【4. 必須環境変数のバリデーション】")

    def validate_required_env_vars():
        """必須環境変数の存在をチェック"""
        required_vars = [
            "DATABASE_URL",
            "JWT_SECRET_KEY",
            "REDIS_URL"
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise EnvironmentError(
                f"必須環境変数が設定されていません: {', '.join(missing_vars)}"
            )

        print("✅ すべての必須環境変数が設定されています")

    # テスト用に環境変数を設定
    os.environ["DATABASE_URL"] = "postgresql://localhost/testdb"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["REDIS_URL"] = "redis://localhost:6379"

    try:
        validate_required_env_vars()
    except EnvironmentError as e:
        print(f"❌ エラー: {e}")


def get_env_as_bool(key: str, default: bool = False) -> bool:
    """環境変数をブール値として取得するヘルパー関数"""
    value = os.getenv(key, "").lower()
    return value in ("true", "1", "yes", "on")


if __name__ == "__main__":
    # 基本操作のデモ
    demonstrate_os_environ()

    # 安全なアクセス方法
    safe_env_access()

    # ベストプラクティス
    environment_variable_best_practices()

    print("\n" + "=" * 50)
    print("まとめ")
    print("=" * 50)
    print("1. 環境変数は外部から設定を渡すメカニズム")
    print("2. 機密情報をコードに書かずに済む")
    print("3. 型変換が必要（すべて文字列として保存される）")
    print("4. 適切なデフォルト値とバリデーションが重要")
    print("5. 命名規則と必須チェックでエラーを防ぐ")
