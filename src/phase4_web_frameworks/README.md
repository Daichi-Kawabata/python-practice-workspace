# フェーズ 4-5: Web フレームワーク基礎・実践学習ガイド

Python Web 開発の基礎から実践までを学習します。FastAPI と Flask の両方を扱い、現代的な Web API 開発手法を習得します。

## 🎯 学習目標

### 基礎目標

- [ ] FastAPI の基本的な使い方を理解する
- [ ] Flask の基本的な使い方を理解する
- [ ] REST API 設計の原則を理解する
- [ ] リクエスト/レスポンスの処理を理解する
- [ ] バリデーション・エラーハンドリングを理解する

### 実践目標

- [ ] 自動 API 文書生成（OpenAPI/Swagger）
- [ ] 非同期処理（async/await）
- [ ] データベース連携（SQLAlchemy）
- [ ] 認証・認可（JWT）
- [ ] テストの書き方（pytest）
- [ ] デプロイ（Docker, Heroku 等）

## 📋 学習内容

### フェーズ 4: Web フレームワーク基礎

#### 4.1 FastAPI 基礎

- **ファイル**: `fastapi_basics/fastapi_hello_world.py`
- **内容**:
  - 基本的なルーティング
  - HTTP メソッド（GET, POST, PUT, DELETE）
  - Pydantic モデル（バリデーション）
  - 自動 API 文書生成
  - クエリパラメータ・パスパラメータ

#### 4.1.1 FastAPI 非同期処理基礎

- **ファイル**: `fastapi_basics/async_basic.py`
- **内容**:
  - async/await の基本概念
  - 同期処理と非同期処理の比較
  - asyncio.gather() による並列処理
  - タイムアウト処理
  - 例外処理

#### 4.1.2 FastAPI 実践的非同期処理

- **ファイル**: `fastapi_basics/async_advanced.py`
- **内容**:
  - HTTP リクエストの非同期処理
  - ファイル操作の非同期処理
  - バックグラウンドタスク
  - 複合的な非同期処理
  - パフォーマンス最適化

#### 4.1.3 FastAPI 非同期処理演習

- **ファイル**: `exercises/async_exercises.py`
- **解答例**: `exercises/async_exercises_solutions.py`
- **内容**:
  - 基本的な非同期関数の実装
  - 複数の非同期処理の並列実行
  - 優先度付きタスクの処理
  - エラーハンドリング
  - タイムアウト処理
  - 結果のキャッシュ

#### 4.2 Flask 基礎

- **ファイル**: `flask_basics/flask_hello_world.py`
- **内容**:
  - 基本的なルーティング
  - HTTP メソッド処理
  - JSON API 作成
  - エラーハンドリング
  - CORS 設定

### フェーズ 5: 実践的な Web API 開発

#### 5.1 データベース連携

- SQLAlchemy との統合
- CRUD 操作の実装
- マイグレーション管理

#### 5.2 認証・認可

- JWT 認証の実装
- ユーザーセッション管理
- 権限制御

#### 5.3 非同期処理

- async/await の基本
- 非同期データベース操作
- 非同期 HTTP 通信

#### 5.4 テスト

- pytest 基本
- API テスト
- モックとフィクスチャ

## 🚀 実習の進め方

### Step 1: 基本的な Web サーバーの起動

#### FastAPI の実行

```bash
# ディレクトリ移動
cd src/phase4_web_frameworks/fastapi_basics

# サーバー起動
python fastapi_hello_world.py
```

アクセス先:

- **アプリケーション**: http://localhost:8000
- **API 文書（Swagger）**: http://localhost:8000/docs
- **API 文書（ReDoc）**: http://localhost:8000/redoc

#### Flask の実行

```bash
# ディレクトリ移動
cd src/phase4_web_frameworks/flask_basics

# サーバー起動
python flask_hello_world.py
```

アクセス先:

- **アプリケーション**: http://localhost:5000

### Step 2: API 動作確認

#### 基本的なエンドポイント

1. `GET /` - ルートエンドポイント
2. `GET /health` - ヘルスチェック
3. `GET /users` - ユーザー一覧
4. `POST /users` - ユーザー作成
5. `GET /users/{user_id}` - ユーザー詳細
6. `PUT /users/{user_id}` - ユーザー更新
7. `DELETE /users/{user_id}` - ユーザー削除

#### curl でのテスト例

```bash
# ユーザー一覧取得
curl http://localhost:8000/users

# ユーザー作成
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "山田太郎",
    "email": "yamada@example.com",
    "age": 28
  }'

# ユーザー詳細取得
curl http://localhost:8000/users/1

# ユーザー更新
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "山田次郎",
    "age": 29
  }'

# ユーザー削除
curl -X DELETE http://localhost:8000/users/1
```

### Step 3: FastAPI vs Flask 比較

| 項目               | FastAPI            | Flask      |
| ------------------ | ------------------ | ---------- |
| **パフォーマンス** | 高速（async 対応） | 中程度     |
| **型安全性**       | 高い（Pydantic）   | 低い       |
| **API 文書生成**   | 自動生成           | 手動       |
| **学習コスト**     | 中程度             | 低い       |
| **エコシステム**   | 新しい             | 成熟       |
| **非同期処理**     | ネイティブ対応     | 拡張が必要 |

## 📚 学習リソース

### 公式ドキュメント

- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [Flask 公式ドキュメント](https://flask.palletsprojects.com/)
- [Pydantic 公式ドキュメント](https://pydantic-docs.helpmanual.io/)

### 推奨記事・チュートリアル

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [REST API 設計ガイド](https://restfulapi.net/)

## 🔧 開発環境セットアップ

### 必要なパッケージ

```bash
# 基本パッケージ
pip install fastapi uvicorn flask flask-cors

# 開発・テスト用パッケージ
pip install pytest pytest-asyncio httpx requests

# データベース関連
pip install sqlalchemy alembic

# 認証関連
pip install python-jose[cryptography] passlib[bcrypt]
```

### VS Code 設定

推奨拡張機能:

- **REST Client** - API テスト用
- **Thunder Client** - API テスト用（Postman 代替）

## 🎯 演習課題

### 課題 1: 基本 API 作成

**難易度**: ★☆☆

- [ ] FastAPI でシンプルな CRUD API を作成
- [ ] Pydantic によるバリデーション
- [ ] エラーハンドリングの実装

### 課題 2: データベース連携

**難易度**: ★★☆

- [ ] SQLAlchemy との統合
- [ ] データベース CRUD 操作
- [ ] マイグレーション管理

### 課題 3: 認証付き API

**難易度**: ★★★

- [ ] JWT 認証の実装
- [ ] ユーザー登録・ログイン
- [ ] 権限制御

### 課題 4: 非同期処理

**難易度**: ★★★

- [ ] 非同期データベース操作
- [ ] 非同期 HTTP 通信
- [ ] 並行処理の実装

### 課題 5: テスト

**難易度**: ★★☆

- [ ] pytest 基本
- [ ] API テスト
- [ ] カバレッジ測定

## 📋 進捗チェックリスト

### 基礎学習

- [ ] FastAPI の基本構造を理解
- [ ] Flask の基本構造を理解
- [ ] HTTP メソッドの使い分けを理解
- [ ] JSON API 設計を理解
- [ ] バリデーションの実装方法を理解

### 実践学習

- [ ] データベース連携の実装
- [ ] 認証システムの実装
- [ ] 非同期処理の実装
- [ ] テストコードの作成
- [ ] API 文書の作成

### 発展学習

- [ ] マイクロサービス設計
- [ ] Docker 化
- [ ] CI/CD 設定
- [ ] 本番環境へのデプロイ

## 🚨 注意事項

### セキュリティ

- 本番環境では必ず HTTPS を使用
- 機密情報は環境変数で管理
- 入力値は必ずバリデーション

### パフォーマンス

- データベースクエリの最適化
- 適切なキャッシュの実装
- 非同期処理の活用

### 保守性

- 適切なエラーハンドリング
- ログ出力の実装
- テストコードの作成

頑張って学習を進めてください！🎉
