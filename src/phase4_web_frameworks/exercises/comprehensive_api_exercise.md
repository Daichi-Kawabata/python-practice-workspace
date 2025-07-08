# 総合演習課題: FastAPI + SQLAlchemy + JWT認証 REST API

## 🎯 目標

FastAPI、SQLAlchemy、JWT認証を組み合わせた実践的なREST APIを構築し、以下のスキルを習得する：

1. **認証付きREST API の構築**
2. **Swagger/OpenAPI ドキュメントの自動生成**
3. **ORMとの連携によるデータ永続化**
4. **実際の開発プロセスの体験**

## 📋 課題概要

**テーマ**: 「シンプルなタスク管理API（Todo API）」

### 主要機能
- ユーザー登録・ログイン（JWT認証）
- タスクのCRUD操作（作成・読み取り・更新・削除）
- ユーザーごとのタスク管理
- API ドキュメントの自動生成

### 技術スタック
- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **Alembic**: データベースマイグレーション
- **JWT**: 認証
- **pytest**: テスト
- **SQLite**: データベース（開発用）

## 🏗️ プロジェクト構造

```
todo_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーション
│   ├── database.py          # データベース設定
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # ユーザーモデル
│   │   └── task.py          # タスクモデル
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydanticスキーマ
│   │   └── task.py          # Pydanticスキーマ
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # 認証関連エンドポイント
│   │   └── tasks.py         # タスク関連エンドポイント
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 設定
│   │   ├── security.py      # JWT認証
│   │   └── dependencies.py  # 依存性注入
│   └── crud/
│       ├── __init__.py
│       ├── user.py          # ユーザーCRUD
│       └── task.py          # タスクCRUD
├── alembic/                 # マイグレーションファイル
├── tests/                   # テストファイル
├── alembic.ini             # Alembic設定
├── requirements.txt        # 依存関係
└── README.md              # プロジェクト説明
```

## 📊 データモデル

### User（ユーザー）
```python
- id: int (Primary Key)
- username: str (Unique)
- email: str (Unique) 
- hashed_password: str
- is_active: bool
- created_at: datetime
- updated_at: datetime
```

### Task（タスク）
```python
- id: int (Primary Key)
- title: str
- description: str (Optional)
- completed: bool
- priority: str (low/medium/high)
- due_date: datetime (Optional)
- user_id: int (Foreign Key)
- created_at: datetime
- updated_at: datetime
```

## 🛠️ 実装要件

### Phase 1: プロジェクトセットアップ
1. ディレクトリ構造の作成
2. 依存関係のインストール
3. データベース設定
4. 基本的なFastAPIアプリケーション

### Phase 2: データベース・モデル
1. SQLAlchemyモデルの実装
2. Alembicの設定とマイグレーション
3. データベース接続の設定

### Phase 3: 認証システム
1. JWT認証の実装
2. ユーザー登録・ログインエンドポイント
3. パスワードハッシュ化
4. 認証ミドルウェア

### Phase 4: CRUD API
1. タスクのCRUD操作
2. ユーザーごとのデータ分離
3. エラーハンドリング
4. バリデーション

### Phase 5: API ドキュメント・テスト
1. Swagger/OpenAPI ドキュメントの確認
2. API エンドポイントのテスト
3. 統合テストの作成

## 🔧 API エンドポイント仕様

### 認証エンドポイント
```
POST /auth/register     # ユーザー登録
POST /auth/login        # ログイン（トークン取得）
GET  /auth/me          # 現在のユーザー情報
```

### タスクエンドポイント
```
GET    /tasks          # タスク一覧取得
POST   /tasks          # タスク作成
GET    /tasks/{id}     # 特定タスク取得
PUT    /tasks/{id}     # タスク更新
DELETE /tasks/{id}     # タスク削除
GET    /tasks/stats    # タスク統計情報
```

### レスポンス例

#### ユーザー登録
```json
POST /auth/register
{
  "username": "testuser",
  "email": "test@example.com", 
  "password": "securepassword"
}

Response:
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true
}
```

#### タスク作成
```json
POST /tasks
Authorization: Bearer <jwt_token>
{
  "title": "新しいタスク",
  "description": "タスクの詳細説明",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59"
}

Response:
{
  "id": 1,
  "title": "新しいタスク",
  "description": "タスクの詳細説明", 
  "completed": false,
  "priority": "high",
  "due_date": "2024-12-31T23:59:59",
  "user_id": 1,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

## ✅ 完了基準

### 必須要件
- [ ] FastAPIアプリケーションが正常に起動する
- [ ] データベースマイグレーションが動作する
- [ ] ユーザー登録・ログインができる
- [ ] JWT認証が正しく動作する
- [ ] タスクのCRUD操作がすべて動作する
- [ ] ユーザーは自分のタスクのみアクセス可能
- [ ] Swagger UIでAPI ドキュメントが確認できる
- [ ] 基本的なテストが通る

### 発展要件（時間があれば）
- [ ] タスクの検索・フィルタ機能
- [ ] ページネーション
- [ ] タスクの優先度・期限による並び替え
- [ ] ユーザープロファイル更新機能
- [ ] 包括的なテストカバレッジ

## 🚀 開始方法

1. **Phase 1から順番に実装**
2. **各Phaseで動作確認**
3. **問題が発生したら前回の教材を参考**
4. **Swagger UI（/docs）で動作確認**

## 📚 参考資料

- **FastAPI公式ドキュメント**: https://fastapi.tiangolo.com/
- **SQLAlchemy公式ドキュメント**: https://docs.sqlalchemy.org/
- **JWT実装**: 今回学習したjwt_auth_basic.pyを参考
- **テスト実装**: pytest_testing_basic.pyを参考

## 💡 学習のポイント

1. **段階的実装**: 一度にすべてを実装せず、段階的に進める
2. **動作確認**: 各機能を実装したら必ずテストする
3. **エラーハンドリング**: 適切な例外処理とHTTPステータスコード
4. **コード品質**: 型ヒント、ドキュメント、テストを意識
5. **実務スキル**: 実際の開発プロセスを体験

頑張って実装してください！わからないことがあれば、いつでも質問してください。🚀
