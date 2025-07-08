# Phase 1: プロジェクトセットアップ

## 🎯 目標
FastAPI + SQLAlchemy + JWT認証のプロジェクト基盤を構築する

## 📁 ディレクトリ構造を作成

```bash
todo_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーションエントリーポイント
│   ├── database.py          # データベース設定・接続
│   ├── models/              # SQLAlchemyモデル
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/             # Pydanticモデル（APIリクエスト・レスポンス）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/             # APIエンドポイント
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── core/                # 設定・ユーティリティ
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   └── crud/                # データベース操作
│       ├── __init__.py
│       ├── user.py
│       └── task.py
├── tests/                   # テストファイル
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt         # 依存関係
└── README.md               # プロジェクト説明
```

## 📦 必要な依存関係

```txt
fastapi==0.116.0
uvicorn==0.35.0
sqlalchemy==2.0.41
alembic==1.16.2
python-jose[cryptography]==3.5.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20
pytest==8.4.1
httpx==0.28.1
```

## 🚀 実装手順

### 1. ディレクトリとファイルを作成
上記の構造でフォルダとファイル（空のものでOK）を作成してください。

### 2. requirements.txt を作成
依存関係をインストールしてください。

### 3. 基本的な main.py を作成
最小限のFastAPIアプリケーションを作成してください。

### 4. データベース設定を準備
SQLAlchemy の基本設定を database.py に記述してください。

## ✅ 完了確認

- [ ] ディレクトリ構造が正しく作成されている
- [ ] 必要なパッケージがインストールされている
- [ ] FastAPIアプリケーションが起動する
- [ ] http://localhost:8000/docs でSwagger UIが表示される

## 💡 ヒント

1. **段階的に進める**: 最初は最小限の実装から始めて、徐々に機能を追加
2. **動作確認**: 各ステップで動作確認を行う
3. **参考教材**: これまでの教材（jwt_auth_basic.py等）を参考にする

次のPhase 2では、データベースモデルとマイグレーションを実装します。
