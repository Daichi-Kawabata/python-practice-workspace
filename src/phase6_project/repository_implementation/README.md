# Repository パターンの実装例

このディレクトリには、ToDo アプリケーションで Repository パターンを実装した例が含まれています。

## ファイル構成

```
repository_implementation/
├── README.md                    # このファイル
├── interfaces/                  # Repository インターフェース
│   ├── __init__.py
│   ├── base_repository.py      # 基底リポジトリインターフェース
│   ├── task_repository.py      # Taskリポジトリインターフェース
│   └── user_repository.py      # Userリポジトリインターフェース
├── implementations/             # Repository 実装
│   ├── __init__.py
│   ├── sqlalchemy_task_repository.py  # SQLAlchemy実装
│   ├── sqlalchemy_user_repository.py  # SQLAlchemy実装
│   └── mock_repositories.py           # テスト用モック実装
├── services/                    # Service層
│   ├── __init__.py
│   ├── task_service.py         # Taskサービス
│   └── user_service.py         # Userサービス
├── controllers/                 # Controller層
│   ├── __init__.py
│   └── task_controller.py      # TaskController
├── main.py                      # FastAPIアプリケーション
└── dependency_injection.py     # 依存性注入の設定
```

## Repository パターンの利点

1. **テスタビリティ**: モックによるテストが容易
2. **保守性**: データアクセスロジックが集約
3. **柔軟性**: 異なるデータストレージへの切り替えが容易
4. **再利用性**: 複数のサービスで共通利用

## 実装のポイント

1. **抽象化**: インターフェースで実装の詳細を隠蔽
2. **依存性の逆転**: 上位層は抽象に依存
3. **単一責任**: 各リポジトリは単一のエンティティを担当
4. **依存性注入**: DI コンテナで依存関係を管理

## アーキテクチャ

### レイヤー構成

```
┌─────────────────┐
│   Controller    │ ← HTTP リクエスト処理
│   (Router)      │   FastAPI エンドポイント
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    Service      │ ← ビジネスロジック
│                 │   複数Repository の協調
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Repository    │ ← データアクセス抽象化
│   (Interface)   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Implementation  │ ← 具体的実装
│ (SQLAlchemy)    │   (SQLAlchemy/Mock)
└─────────────────┘
```

### データフロー

1. **HTTP Request** → **Controller** → **Service** → **Repository** → **Database**
2. **Database** → **Repository** → **Service** → **Controller** → **HTTP Response**

## 各層の責任

### Controller 層

- HTTP リクエストの受信と処理
- Service 層のメソッド呼び出し
- HTTP レスポンスの構築
- エラーハンドリングと HTTP ステータスコード設定

### Service 層

- ビジネスロジックの実装
- 複数 Repository の協調
- トランザクション管理
- データの整合性保証

### Repository 層

- データアクセスロジックの抽象化
- CRUD 操作の定義
- クエリロジックの実装

## 学習の進め方

1. **interfaces/** でインターフェースの定義を理解
2. **implementations/** で具体的実装を確認
3. **services/** でビジネスロジックの実装を学習
4. **controllers/** で HTTP エンドポイントの実装を確認
5. **main.py** でアプリケーション全体の統合を理解
6. 依存性注入とテストの容易さを体験

## 実行方法

```bash
# 必要なパッケージのインストール
pip install fastapi uvicorn sqlalchemy

# アプリケーションの起動
python main.py

# またはuvicornを使用
uvicorn main:app --reload
```

## API エンドポイント

- `POST /tasks/` - タスク作成
- `GET /tasks/` - タスク一覧取得
- `GET /tasks/{task_id}` - タスク詳細取得
- `PUT /tasks/{task_id}` - タスク更新
- `DELETE /tasks/{task_id}` - タスク削除
- `POST /tasks/{task_id}/complete` - タスク完了
- `GET /tasks/search` - タスク検索
- `GET /tasks/statistics` - 統計情報取得
