# Phase 2: データベース・モデル実装

## 🎯 目標
SQLAlchemyモデルとAlembicマイグレーションを実装する

## 📊 実装するモデル

### User モデル
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
```

### Task モデル
```python
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    owner = relationship("User", back_populates="tasks")
```

## 🗃️ 実装手順

### 1. database.py の実装
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLiteデータベースURL（開発用）
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_api.db"

# データベースエンジンの作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite用
)

# セッションファクトリーの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()

# データベース依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. models/user.py の実装
- 上記のUserモデルを実装してください
- 必要なimport文も含めてください

### 3. models/task.py の実装  
- 上記のTaskモデルを実装してください
- ユーザーとのリレーションシップを正しく設定してください

### 4. models/__init__.py の実装
```python
from .user import User
from .task import Task

__all__ = ["User", "Task"]
```

### 5. Alembic の設定
```bash
# Alembicの初期化
alembic init alembic

# alembic.ini の設定
sqlalchemy.url = sqlite:///./todo_api.db

# alembic/env.py の設定
from app.models import Base
target_metadata = Base.metadata
```

### 6. 初回マイグレーション
```bash
# マイグレーションファイルの生成
alembic revision --autogenerate -m "Create users and tasks tables"

# マイグレーションの実行
alembic upgrade head
```

## 🔍 Pydantic スキーマの実装

### schemas/user.py
```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

### schemas/task.py  
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium" 
    high = "high"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.medium
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

## ✅ 完了確認

- [ ] SQLAlchemyモデルが正しく実装されている
- [ ] Alembicの設定が完了している
- [ ] データベースマイグレーションが成功している
- [ ] Pydanticスキーマが実装されている
- [ ] リレーションシップが正しく設定されている

## 🧪 動作確認方法

```python
# データベース接続テスト
from app.database import engine, Base
from app.models import User, Task

# テーブル作成確認
Base.metadata.create_all(bind=engine)

# データベースファイルの確認
# todo_api.db ファイルが作成されていることを確認
```

## 💡 実装のポイント

1. **型ヒント**: すべてのフィールドに適切な型ヒントを付ける
2. **制約**: 必要なNull制約、Unique制約を設定
3. **リレーション**: 1対多の関係を正しく実装
4. **タイムスタンプ**: 作成日時・更新日時を自動設定
5. **Enum**: 優先度はEnumを使用して型安全性を確保

次のPhase 3では、JWT認証システムを実装します。
