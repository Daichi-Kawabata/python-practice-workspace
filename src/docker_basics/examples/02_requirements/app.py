#!/usr/bin/env python3
"""
依存関係を含むPythonアプリケーション

外部ライブラリ（requests, pandas）を使用したサンプルアプリケーション
"""

import sys
import os
from datetime import datetime
import requests
import pandas as pd
import json


def fetch_weather_data():
    """公開APIから天気データを取得（例）"""
    try:
        # JSONPlaceholderの公開APIを使用（実際の天気APIの代替）
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return {
            "success": True,
            "data": data,
            "message": "API接続成功"
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "API接続失敗"
        }


def analyze_sample_data():
    """pandasを使ったサンプルデータ分析"""
    # サンプルデータの作成
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 22],
        'score': [85, 92, 78, 96, 88],
        'city': ['Tokyo', 'Osaka', 'Tokyo', 'Kyoto', 'Tokyo']
    }

    df = pd.DataFrame(data)

    # 基本統計
    stats = {
        "total_records": len(df),
        "average_age": df['age'].mean(),
        "average_score": df['score'].mean(),
        "max_score": df['score'].max(),
        "min_score": df['score'].min(),
        "tokyo_count": len(df[df['city'] == 'Tokyo'])
    }

    return df, stats


def main():
    """メイン関数"""
    print("=" * 60)
    print("🐍 Python Docker Example with Dependencies")
    print("=" * 60)

    # 基本情報
    print(f"🕐 現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python バージョン: {sys.version.split()[0]}")

    # インストールされたライブラリのバージョン確認
    print(f"📦 requests バージョン: {requests.__version__}")
    print(f"📊 pandas バージョン: {pd.__version__}")

    # 環境変数の確認
    app_env = os.environ.get('APP_ENV', 'development')
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    print(f"🌍 環境: {app_env}")
    print(f"🐛 デバッグモード: {debug_mode}")

    print("\n" + "=" * 60)
    print("📡 API接続テスト")
    print("=" * 60)

    # API接続テスト
    api_result = fetch_weather_data()
    if api_result["success"]:
        print("✅", api_result["message"])
        if debug_mode:
            print(
                f"📋 取得データ: {json.dumps(api_result['data'], indent=2, ensure_ascii=False)}")
    else:
        print("❌", api_result["message"])
        print(f"🚨 エラー: {api_result['error']}")

    print("\n" + "=" * 60)
    print("📊 データ分析例")
    print("=" * 60)

    # データ分析例
    df, stats = analyze_sample_data()

    print("📋 サンプルデータ:")
    print(df.to_string(index=False))

    print(f"\n📈 統計情報:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    # 環境固有の処理
    if app_env == "production":
        print("\n🚀 本番環境モードで実行中")
    elif app_env == "development":
        print("\n🛠️  開発環境モードで実行中")
        if debug_mode:
            print("🔍 詳細デバッグ情報:")
            print(f"   データフレーム形状: {df.shape}")
            print(f"   データ型: {df.dtypes.to_dict()}")

    print("\n✅ アプリケーション実行完了!")


if __name__ == "__main__":
    main()
