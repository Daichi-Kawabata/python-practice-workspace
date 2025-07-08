# FastAPI + SQLAlchemy 実践演習課題

## 🎯 目標

SQLAlchemyを使ったデータベース操作とFastAPIを組み合わせた実践的なAPI開発を学習する

---

## 演習1: データベース接続とモデル定義（基礎）

### 目標
SQLAlchemyを使用したデータベース接続とモデル定義を理解する

### 課題内容

1. **データベース設定**
   - SQLiteデータベースの接続設定
   - セッション管理の実装

2. **基本モデルの作成**
   - User（ユーザー）モデル
   - Post（投稿）モデル
   - リレーションシップの定義

### ファイル構成
```
exercise1/
├── database.py      # データベース設定
├── models.py        # SQLAlchemyモデル
├── main.py          # FastAPIアプリ
└── requirements.txt
```

### 実装例

**database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./exercise1.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**models.py**
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーションシップ
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # リレーションシップ
    author = relationship("User", back_populates="posts")
```

**main.py**
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
import models

# テーブル作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exercise 1: Database Connection")

@app.get("/")
def read_root():
    return {"message": "Database connection exercise"}

@app.get("/users/count")
def get_users_count(db: Session = Depends(get_db)):
    count = db.query(models.User).count()
    return {"users_count": count}

@app.get("/posts/count")
def get_posts_count(db: Session = Depends(get_db)):
    count = db.query(models.Post).count()
    return {"posts_count": count}
```

### チェックポイント
- [ ] データベースファイルが作成される
- [ ] テーブルが正しく作成される
- [ ] カウントエンドポイントが動作する
- [ ] リレーションシップが正しく設定されている

---

## 演習2: CRUD操作の実装（初級〜中級）

### 目標
SQLAlchemyを使った基本的なCRUD操作をFastAPIと組み合わせて実装する

### 課題内容

1. **Pydanticスキーマの作成**
   - リクエスト/レスポンス用スキーマ

2. **CRUD操作の実装**
   - ユーザーの作成・読み取り・更新・削除
   - 投稿の作成・読み取り・更新・削除

### 追加ファイル

**schemas.py**
```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    posts: List['Post'] = []

    class Config:
        from_attributes = True

# Post schemas
class PostBase(BaseModel):
    title: str
    content: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    author: User

    class Config:
        from_attributes = True

# Forward reference update
User.model_rebuild()
```

**crud.py**
```python
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
import schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Post CRUD operations
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Post).filter(
        models.Post.author_id == user_id
    ).offset(skip).limit(limit).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
```

**main.py（更新版）**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
import models
import schemas
import crud

# テーブル作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exercise 2: CRUD Operations")

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Post endpoints
@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_post(db=db, post=post, user_id=user_id)

@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.get("/users/{user_id}/posts/", response_model=List[schemas.Post])
def read_posts_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return posts

@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id=post_id, post_update=post_update)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
```

### チェックポイント
- [ ] 全てのCRUD操作が動作する
- [ ] リレーションシップが正しく動作する（ユーザーの投稿一覧など）
- [ ] バリデーションエラーが適切に処理される
- [ ] 重複データの処理が適切に行われる

---

## 演習3: 高度なクエリとフィルタリング（中級）

### 目標
SQLAlchemyの高度なクエリ機能を使った検索・フィルタリング機能を実装する

### 課題内容

1. **検索機能の実装**
   - タイトルや内容での部分一致検索
   - 複数条件での検索

2. **フィルタリング機能**
   - 日付範囲での絞り込み
   - 作成者での絞り込み

3. **ソート機能**
   - 作成日、更新日、タイトルでのソート

4. **ページネーション**
   - ページベースのページネーション

### 実装例（追加機能）

**crud.py（拡張版）**
```python
from sqlalchemy import or_, and_, desc, asc
from datetime import datetime
from typing import Optional

def search_posts(
    db: Session,
    query: Optional[str] = None,
    author_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
    skip: int = 0,
    limit: int = 100
):
    """
    高度な投稿検索機能
    """
    db_query = db.query(models.Post)
    
    # テキスト検索
    if query:
        db_query = db_query.filter(
            or_(
                models.Post.title.contains(query),
                models.Post.content.contains(query)
            )
        )
    
    # 作成者フィルタ
    if author_id:
        db_query = db_query.filter(models.Post.author_id == author_id)
    
    # 日付範囲フィルタ
    if start_date:
        db_query = db_query.filter(models.Post.created_at >= start_date)
    if end_date:
        db_query = db_query.filter(models.Post.created_at <= end_date)
    
    # ソート
    if sort_by == "created_at":
        sort_column = models.Post.created_at
    elif sort_by == "updated_at":
        sort_column = models.Post.updated_at
    elif sort_by == "title":
        sort_column = models.Post.title
    else:
        sort_column = models.Post.created_at
    
    if sort_order == "desc":
        db_query = db_query.order_by(desc(sort_column))
    else:
        db_query = db_query.order_by(asc(sort_column))
    
    # ページネーション
    total = db_query.count()
    posts = db_query.offset(skip).limit(limit).all()
    
    return {
        "posts": posts,
        "total": total,
        "page": (skip // limit) + 1,
        "pages": (total + limit - 1) // limit
    }

def get_post_stats(db: Session):
    """
    投稿統計情報を取得
    """
    from sqlalchemy import func
    
    stats = db.query(
        func.count(models.Post.id).label("total_posts"),
        func.count(models.Post.author_id.distinct()).label("total_authors"),
        func.avg(func.length(models.Post.content)).label("avg_content_length")
    ).first()
    
    return {
        "total_posts": stats.total_posts,
        "total_authors": stats.total_authors,
        "average_content_length": round(stats.avg_content_length or 0, 2)
    }
```

**schemas.py（拡張版）**
```python
from typing import Optional
from datetime import datetime

class PostSearchParams(BaseModel):
    query: Optional[str] = None
    author_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: Optional[int] = 1
    page_size: Optional[int] = 10

class PostSearchResult(BaseModel):
    posts: List[Post]
    total: int
    page: int
    pages: int
```

**main.py（拡張版エンドポイント追加）**
```python
@app.get("/posts/search", response_model=schemas.PostSearchResult)
def search_posts(
    query: Optional[str] = None,
    author_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    高度な投稿検索API
    """
    skip = (page - 1) * page_size
    result = crud.search_posts(
        db=db,
        query=query,
        author_id=author_id,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=page_size
    )
    return result

@app.get("/posts/stats")
def get_post_statistics(db: Session = Depends(get_db)):
    """
    投稿統計情報API
    """
    return crud.get_post_stats(db)
```

### チェックポイント
- [ ] テキスト検索が動作する
- [ ] 複数条件でのフィルタリングが動作する
- [ ] ソート機能が動作する
- [ ] ページネーションが正しく実装されている
- [ ] 統計情報が正しく計算される

---

## 演習4: トランザクションとエラーハンドリング（中級〜上級）

### 目標
データベーストランザクションを理解し、複数操作の整合性を保つ方法を学ぶ

### 課題内容

1. **トランザクション管理**
   - 複数テーブルへの同時更新
   - ロールバック処理

2. **エラーハンドリング**
   - データベースエラーの適切な処理
   - 重複エラー、外部キー制約エラーなど

3. **バッチ処理**
   - 一括データ挿入
   - 大量データの効率的な処理

### 実装例

**crud.py（トランザクション版）**
```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from contextlib import contextmanager

@contextmanager
def db_transaction(db: Session):
    """
    データベーストランザクション管理
    """
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

def transfer_posts(db: Session, from_user_id: int, to_user_id: int):
    """
    投稿を別のユーザーに移譲（トランザクション例）
    """
    try:
        with db_transaction(db):
            # ユーザーの存在確認
            from_user = get_user(db, from_user_id)
            to_user = get_user(db, to_user_id)
            
            if not from_user or not to_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # 投稿の移譲
            posts = db.query(models.Post).filter(models.Post.author_id == from_user_id).all()
            for post in posts:
                post.author_id = to_user_id
            
            return {"transferred_posts": len(posts)}
    
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Database integrity error")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

def bulk_create_posts(db: Session, posts_data: List[schemas.PostCreate], user_id: int):
    """
    投稿の一括作成
    """
    try:
        with db_transaction(db):
            db_posts = []
            for post_data in posts_data:
                db_post = models.Post(**post_data.dict(), author_id=user_id)
                db_posts.append(db_post)
            
            db.bulk_save_objects(db_posts)
            return {"created_posts": len(db_posts)}
    
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Bulk insert failed due to data constraints")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error during bulk insert")
```

**main.py（エラーハンドリング追加）**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity constraint violated"}
    )

@app.post("/users/{from_user_id}/transfer-posts/{to_user_id}")
def transfer_user_posts(from_user_id: int, to_user_id: int, db: Session = Depends(get_db)):
    """
    投稿移譲API（トランザクション例）
    """
    return crud.transfer_posts(db, from_user_id, to_user_id)

@app.post("/users/{user_id}/posts/bulk")
def bulk_create_posts(
    user_id: int, 
    posts: List[schemas.PostCreate], 
    db: Session = Depends(get_db)
):
    """
    投稿一括作成API
    """
    return crud.bulk_create_posts(db, posts, user_id)
```

### チェックポイント
- [ ] トランザクションが正しく動作する
- [ ] エラー時にロールバックが実行される
- [ ] 適切なエラーレスポンスが返される
- [ ] バッチ処理が効率的に実行される

---

## 🏆 最終課題: パフォーマンス最適化

### 目標
大量データでのパフォーマンス最適化技術を学ぶ

### 課題内容

1. **クエリ最適化**
   - N+1問題の解決（eager loading）
   - インデックスの活用

2. **接続プールの設定**
   - 適切な接続プール設定

3. **キャッシュ戦略**
   - クエリ結果のキャッシュ

### 実装例

**models.py（インデックス追加）**
```python
from sqlalchemy import Index

class Post(Base):
    __tablename__ = "posts"
    
    # 既存のカラム定義...
    
    # インデックス定義
    __table_args__ = (
        Index('idx_posts_author_created', 'author_id', 'created_at'),
        Index('idx_posts_title', 'title'),
    )
```

**crud.py（最適化版）**
```python
from sqlalchemy.orm import joinedload

def get_posts_with_authors(db: Session, skip: int = 0, limit: int = 100):
    """
    N+1問題を解決した投稿取得（eager loading）
    """
    return db.query(models.Post).options(
        joinedload(models.Post.author)
    ).offset(skip).limit(limit).all()

# キャッシュ機能（簡単な実装例）
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_cached(db: Session, user_id: int):
    """
    ユーザー情報のキャッシュ取得
    """
    return db.query(models.User).filter(models.User.id == user_id).first()
```

**database.py（接続プール設定）**
```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=20,          # 接続プールサイズ
    max_overflow=30,       # 最大オーバーフロー接続数
    pool_pre_ping=True,    # 接続確認
    pool_recycle=3600      # 接続リサイクル時間（秒）
)
```

### チェックポイント
- [ ] N+1問題が解決されている
- [ ] インデックスが適切に設定されている
- [ ] 接続プールが適切に設定されている
- [ ] クエリパフォーマンスが改善されている

---

## 🎯 学習成果確認

これらの演習を完了したら、以下の技術に習熟しているはずです：

1. **SQLAlchemy ORM**
   - モデル定義とリレーションシップ
   - 基本的なCRUD操作
   - 高度なクエリ操作

2. **FastAPI + SQLAlchemy統合**
   - 依存性注入を使ったデータベースセッション管理
   - Pydanticスキーマとの連携
   - エラーハンドリング

3. **データベース設計**
   - 適切なインデックス設計
   - トランザクション管理
   - パフォーマンス最適化

次は `comprehensive_api_exercise.md` の総合演習に挑戦してください！
