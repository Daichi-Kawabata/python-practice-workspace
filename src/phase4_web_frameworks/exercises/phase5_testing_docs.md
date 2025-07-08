# Phase 5: テスト・ドキュメント・最終確認

## 🎯 目標
API の動作確認、テストの実装、ドキュメントの充実を行い、プロジェクトを完成させる

## 📋 実装する項目

1. **API テストの実装**
2. **Swagger ドキュメントの最適化**
3. **エラーハンドリングの改善**
4. **パフォーマンスの確認**
5. **デプロイ準備**

## 🧪 テストの実装

### 1. tests/conftest.py の実装
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.models.task import Task

# テスト用SQLiteデータベース（インメモリ）
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """テスト用データベースセッション"""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """テスト用FastAPIクライアント"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """テスト用ユーザー"""
    from app.crud.user import create_user
    from app.schemas.user import UserCreate
    
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    return create_user(db=db_session, user=user_data)

@pytest.fixture
def auth_headers(client, test_user):
    """認証ヘッダー"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### 2. tests/test_auth.py の実装
```python
import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """ユーザー登録テスト"""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_register_duplicate_user(client: TestClient, test_user):
    """重複ユーザー登録テスト"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 400

def test_login_user(client: TestClient, test_user):
    """ログインテスト"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user):
    """無効な認証情報でのログインテスト"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_get_current_user(client: TestClient, auth_headers):
    """現在のユーザー取得テスト"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
```

### 3. tests/test_tasks.py の実装
```python
import pytest
from fastapi.testclient import TestClient

def test_create_task(client: TestClient, auth_headers):
    """タスク作成テスト"""
    response = client.post(
        "/tasks/",
        json={
            "title": "テストタスク",
            "description": "テスト用のタスクです",
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["completed"] == False
    assert data["priority"] == "high"

def test_get_tasks(client: TestClient, auth_headers):
    """タスク一覧取得テスト"""
    # タスクを作成
    client.post(
        "/tasks/",
        json={"title": "タスク1", "priority": "low"},
        headers=auth_headers
    )
    client.post(
        "/tasks/",
        json={"title": "タスク2", "priority": "medium"},
        headers=auth_headers
    )
    
    # 一覧取得
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_task(client: TestClient, auth_headers):
    """タスク更新テスト"""
    # タスク作成
    create_response = client.post(
        "/tasks/",
        json={"title": "更新前タスク", "priority": "low"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # タスク更新
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "更新後タスク", "completed": True},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新後タスク"
    assert data["completed"] == True

def test_delete_task(client: TestClient, auth_headers):
    """タスク削除テスト"""
    # タスク作成
    create_response = client.post(
        "/tasks/",
        json={"title": "削除対象タスク", "priority": "medium"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # タスク削除
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # 削除確認
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_task_stats(client: TestClient, auth_headers):
    """タスク統計テスト"""
    # 複数タスクを作成
    client.post(
        "/tasks/",
        json={"title": "完了タスク", "priority": "high"},
        headers=auth_headers
    )
    task_response = client.post(
        "/tasks/",
        json={"title": "未完了タスク", "priority": "low"},
        headers=auth_headers
    )
    
    # 1つのタスクを完了にする
    task_id = task_response.json()["id"]
    client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=auth_headers
    )
    
    # 統計取得
    response = client.get("/tasks/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 2
    assert data["completed_tasks"] == 1
    assert data["pending_tasks"] == 1
```

## 📚 Swagger ドキュメントの最適化

### 1. models の改善（ドキュメント用）
```python
# app/models/task.py に追加
class Task(Base):
    __tablename__ = "tasks"
    
    # ... existing fields ...
    
    class Config:
        schema_extra = {
            "example": {
                "title": "プロジェクトの企画書作成",
                "description": "来月のプレゼンテーション用の企画書を作成する",
                "priority": "high",
                "due_date": "2024-01-31T17:00:00"
            }
        }
```

### 2. API エンドポイントにタグと説明を追加
```python
# app/routers/tasks.py の各エンドポイントに以下を追加

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    新しいタスクを作成
    
    - **title**: タスクのタイトル（必須）
    - **description**: タスクの詳細説明（任意）
    - **priority**: 優先度（low/medium/high、デフォルト: medium）
    - **due_date**: 期限（任意）
    """
    return create_task(db=db, task=task, user_id=current_user.id)
```

## 🔧 エラーハンドリングの改善

### 1. カスタム例外クラス
```python
# app/core/exceptions.py
class TodoAPIException(Exception):
    """アプリケーション共通例外"""
    pass

class TaskNotFoundError(TodoAPIException):
    """タスクが見つからない場合の例外"""
    pass

class UserNotFoundError(TodoAPIException):
    """ユーザーが見つからない場合の例外"""
    pass

class DuplicateUserError(TodoAPIException):
    """ユーザーの重複エラー"""
    pass
```

### 2. グローバル例外ハンドラー
```python
# app/main.py に追加
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "タスクが見つかりません"}
    )
```

## ✅ 最終チェックリスト

### 機能面
- [ ] ユーザー登録・ログインが正常に動作する
- [ ] タスクのCRUD操作がすべて動作する
- [ ] 認証・認可が正しく機能する
- [ ] エラーハンドリングが適切に行われる
- [ ] API レスポンスが期待通りの形式

### ドキュメント面
- [ ] Swagger UIでAPIが正しく表示される
- [ ] 各エンドポイントに適切な説明がある
- [ ] サンプルリクエスト・レスポンスが表示される
- [ ] 認証方法が明確に示されている

### テスト面
- [ ] 主要な機能のテストが実装されている
- [ ] テストが正常に実行される
- [ ] エラーケースのテストが含まれている

### セキュリティ面
- [ ] パスワードが適切にハッシュ化されている
- [ ] JWTトークンが正しく検証される
- [ ] ユーザーは自分のデータのみアクセス可能

## 🚀 テスト実行方法

```bash
# すべてのテストを実行
pytest

# 詳細出力でテスト実行
pytest -v

# カバレッジ測定
pytest --cov=app tests/

# 特定のテストファイルのみ実行
pytest tests/test_auth.py
pytest tests/test_tasks.py
```

## 🎉 完成！

すべてのチェックリストが完了したら、Todo API プロジェクトの完成です！

### 学習成果
- ✅ FastAPI を使用したREST API の構築
- ✅ SQLAlchemy によるデータベース操作
- ✅ JWT認証の実装
- ✅ Swagger/OpenAPI ドキュメントの自動生成
- ✅ pytest を使用したAPIテスト
- ✅ 実践的な開発プロセスの体験

### 次のステップ（発展課題）
- Docker化
- CI/CDパイプラインの構築
- 本番環境へのデプロイ
- フロントエンド（React/Vue.js）との連携
- WebSocketを使用したリアルタイム機能

お疲れ様でした！🎊
