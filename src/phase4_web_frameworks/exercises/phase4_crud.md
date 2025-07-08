# Phase 4: タスクCRUD API実装

## 🎯 目標
認証されたユーザーのタスク管理機能（CRUD操作）を実装する

## 📋 実装する機能

1. **タスク一覧取得** (GET /tasks)
2. **タスク作成** (POST /tasks)
3. **個別タスク取得** (GET /tasks/{id})
4. **タスク更新** (PUT /tasks/{id})
5. **タスク削除** (DELETE /tasks/{id})
6. **タスク統計** (GET /tasks/stats)

## 🔧 実装手順

### 1. crud/task.py の実装
```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from datetime import datetime

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks_by_user(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    completed: Optional[bool] = None
) -> List[Task]:
    """ユーザーのタスク一覧を取得"""
    query = db.query(Task).filter(Task.user_id == user_id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    return query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """IDとユーザーIDでタスクを取得（権限チェック含む）"""
    return db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()

def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    """タスクを作成"""
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
    """タスクを更新"""
    db_task = get_task_by_id(db, task_id, user_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    # 更新日時を設定
    db_task.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """タスクを削除"""
    db_task = get_task_by_id(db, task_id, user_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

def get_task_stats(db: Session, user_id: int) -> dict:
    """ユーザーのタスク統計を取得"""
    total_tasks = db.query(Task).filter(Task.user_id == user_id).count()
    completed_tasks = db.query(Task).filter(
        and_(Task.user_id == user_id, Task.completed == True)
    ).count()
    pending_tasks = total_tasks - completed_tasks
    
    # 優先度別統計
    high_priority = db.query(Task).filter(
        and_(Task.user_id == user_id, Task.priority == "high", Task.completed == False)
    ).count()
    
    # 期限切れタスク
    overdue_tasks = db.query(Task).filter(
        and_(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date < datetime.utcnow(),
            Task.due_date.isnot(None)
        )
    ).count()
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "high_priority_pending": high_priority,
        "overdue_tasks": overdue_tasks
    }
```

### 2. routers/tasks.py の実装
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import (
    get_tasks_by_user,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    get_task_stats
)
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=100, description="取得する最大件数"),
    completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """タスク一覧取得"""
    tasks = get_tasks_by_user(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        completed=completed
    )
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """タスク作成"""
    return create_task(db=db, task=task, user_id=current_user.id)

@router.get("/stats")
def read_task_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """タスク統計取得"""
    return get_task_stats(db=db, user_id=current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """個別タスク取得"""
    task = get_task_by_id(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりません"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """タスク更新"""
    task = update_task(db=db, task_id=task_id, task_update=task_update, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりません"
        )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """タスク削除"""
    success = delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりません"
        )
    return None  # 204 No Content
```

### 3. main.py の更新
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, tasks
from app.database import engine
from app.models import Base

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="FastAPI + SQLAlchemy + JWT認証を使用したタスク管理API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    """ルートエンドポイント"""
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "healthy"}
```

## ✅ 完了確認

- [ ] タスクの一覧取得ができる
- [ ] タスクの作成ができる
- [ ] 個別タスクの取得ができる
- [ ] タスクの更新ができる
- [ ] タスクの削除ができる
- [ ] タスク統計が表示される
- [ ] ユーザーは自分のタスクのみアクセス可能
- [ ] 適切なエラーハンドリングがされている

## 🧪 動作確認方法

### 1. Swagger UIでのテスト
1. http://localhost:8000/docs にアクセス
2. 「Authorize」ボタンでJWTトークンを設定
3. 各エンドポイントをテストする

### 2. curl でのテスト例
```bash
# 認証トークンを取得
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword" | jq -r '.access_token')

# タスク作成
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新しいタスク",
    "description": "タスクの説明",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59"
  }'

# タスク一覧取得
curl -X GET "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer $TOKEN"

# タスク統計取得
curl -X GET "http://localhost:8000/tasks/stats" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. テストシナリオ

#### シナリオ1: 基本的なCRUD操作
1. ユーザー登録 → ログイン → タスク作成 → 一覧確認 → 更新 → 削除

#### シナリオ2: フィルタ機能
1. 複数タスクを作成（完了・未完了を混在）
2. 完了状態でフィルタして取得
3. ページネーション機能の確認

#### シナリオ3: 権限チェック
1. 複数ユーザーでタスクを作成
2. 他のユーザーのタスクにアクセスできないことを確認

## 💡 実装のポイント

1. **権限チェック**: すべての操作でユーザーの所有権を確認
2. **エラーハンドリング**: 404、403等の適切なレスポンス
3. **バリデーション**: クエリパラメータの検証
4. **ページネーション**: 大量データに対応
5. **統計情報**: 有用なダッシュボード情報を提供

次のPhase 5では、テストとAPI ドキュメントの最終確認を行います。
