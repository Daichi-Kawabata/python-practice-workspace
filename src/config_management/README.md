# 環境変数管理・設定ファイル学習ガイド

## 学習目標

- 環境変数とは何か、なぜ重要なのかを理解する
- Python での環境変数の読み取り・設定方法を学ぶ
- 設定ファイル（.env、JSON、YAML、TOML）の利用方法を習得する
- Pydantic Settings を使った型安全な設定管理を学ぶ
- 開発/ステージング/本番環境での設定の使い分けを理解する

## 学習内容

### 1. 基本概念

- **環境変数の役割**: 機密情報、環境固有設定の管理
- **12-Factor App**: 設定に関するベストプラクティス
- **設定の種類**: データベース接続、API キー、デバッグモードなど

### 2. Python での実装方法

- **os.environ**: 基本的な環境変数アクセス
- **python-dotenv**: .env ファイルから環境変数をロード
- **configparser**: INI 形式の設定ファイル
- **Pydantic Settings**: 型安全な設定管理

### 3. 実践例

- **FastAPI アプリケーション**: 設定クラスの作成
- **データベース接続**: 環境別の接続文字列
- **ログ設定**: 環境に応じたログレベル
- **セキュリティ設定**: JWT 秘密鍵、CORS 設定

## ファイル構成

```
config_management/
├── README.md                    # このファイル
├── basic_examples/              # 基本的な使用例
│   ├── 01_os_environ.py        # os.environ の基本
│   ├── 02_dotenv_usage.py      # python-dotenv の使用
│   ├── 03_config_files.py      # 各種設定ファイル形式
│   └── 04_pydantic_settings.py # Pydantic Settings
├── practical_examples/          # 実践的な例
│   ├── fastapi_config/         # FastAPI での設定管理
│   ├── database_config/        # データベース設定
│   └── logging_config/         # ログ設定
├── environment_examples/        # 環境別設定例
│   ├── .env.development        # 開発環境
│   ├── .env.staging            # ステージング環境
│   ├── .env.production         # 本番環境（例）
│   └── config.yaml             # YAML 設定例
└── best_practices/             # ベストプラクティス
    ├── security_guidelines.md  # セキュリティガイドライン
    └── deployment_tips.md      # デプロイ時の注意点
```

## 学習の流れ

1. **基本概念の理解** (basic_examples/)
2. **実践的な実装** (practical_examples/)
3. **環境別設定** (environment_examples/)
4. **ベストプラクティス** (best_practices/)

## 前提知識

- Python の基本文法
- FastAPI の基本的な使用方法
- データベース接続の基本概念
