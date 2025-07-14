#!/usr/bin/env python3
"""
シンプルなPythonアプリケーション

このスクリプトは基本的なDockerコンテナ化の学習用です。
"""

import sys
import os
from datetime import datetime


def main():
    """メイン関数"""
    print("=" * 50)
    print("🐍 Python Docker Example")
    print("=" * 50)

    # 基本情報の表示
    print(f"🕐 現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python バージョン: {sys.version}")
    print(f"💻 プラットフォーム: {sys.platform}")

    # 環境変数の表示
    print("\n📋 環境変数:")
    env_vars = ['PATH', 'PYTHONPATH', 'HOME', 'USER', 'APP_ENV']
    for var in env_vars:
        value = os.environ.get(var, '(未設定)')
        print(f"  {var}: {value}")

    # カスタム環境変数があれば表示
    custom_vars = [key for key in os.environ.keys()
                   if key.startswith(('APP_', 'DOCKER_'))]
    if custom_vars:
        print("\n🔧 カスタム環境変数:")
        for var in sorted(custom_vars):
            print(f"  {var}: {os.environ[var]}")

    # 簡単な計算処理
    print("\n🧮 計算例:")
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    average = total / len(numbers)
    print(f"  数列: {numbers}")
    print(f"  合計: {total}")
    print(f"  平均: {average:.2f}")

    print("\n✅ アプリケーション実行完了!")


if __name__ == "__main__":
    main()
