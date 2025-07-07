"""
FastAPI基礎学習 - Hello World & 基本概念

このファイルでは、FastAPIの基本的な使い方を学習します：
- 基本的なルーティング
- HTTPメソッド（GET, POST, PUT, DELETE）
- パスパラメータ & クエリパラメータ
- リクエストボディ（Pydantic）
- レスポンスモデル
- 自動API文書生成
"""

from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# FastAPIアプリケーションの作成
app = FastAPI(
    title="FastAPI基礎学習",
    description="FastAPIの基本的な使い方を学習するためのサンプルアプリケーション",
    version="1.0.0"
)

# --- データモデル（Pydantic） ---


class User(BaseModel):
    """ユーザーモデル"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description="ユーザー名")
    email: str = Field(...,
                       pattern=r'^[^@]+@[^@]+\.[^@]+$', description="メールアドレス")
    age: Optional[int] = Field(None, ge=0, le=150, description="年齢")
    created_at: Optional[datetime] = None


class UserResponse(BaseModel):
    """ユーザーレスポンスモデル"""
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime


class UserCreate(BaseModel):
    """ユーザー作成用モデル"""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    age: Optional[int] = Field(None, ge=0, le=150)


class UserUpdate(BaseModel):
    """ユーザー更新用モデル"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    age: Optional[int] = Field(None, ge=0, le=150)

# --- インメモリデータベース（学習用） ---


users_db: List[User] = []
next_user_id = 1

# --- ルートエンドポイント ---


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "FastAPI基礎学習へようこそ！",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "ok", "timestamp": datetime.now()}

# --- ユーザー管理エンドポイント ---


@app.get("/users", response_model=List[UserResponse])
async def get_users(
    limit: int = Query(10, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット"),
    name_filter: Optional[str] = Query(None, description="名前フィルター")
):
    """ユーザー一覧取得"""
    filtered_users = users_db

    # 名前フィルター
    if name_filter:
        filtered_users = [
            u for u in filtered_users if name_filter.lower() in u.name.lower()]

    # ページネーション
    paginated_users = filtered_users[offset:offset + limit]

    return paginated_users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(..., ge=1, description="ユーザーID")
):
    """ユーザー詳細取得"""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate):
    """ユーザー作成"""
    global next_user_id

    # メールアドレスの重複チェック
    if any(u.email == user_data.email for u in users_db):
        raise HTTPException(status_code=400, detail="メールアドレスが既に存在します")

    # ユーザー作成
    new_user = User(
        id=next_user_id,
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        created_at=datetime.now()
    )

    users_db.append(new_user)
    next_user_id += 1

    return new_user


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., ge=1, description="ユーザーID")
):
    """ユーザー更新"""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    # メールアドレスの重複チェック（他のユーザーとの重複）
    if user_data.email and any(u.email == user_data.email and u.id != user_id for u in users_db):
        raise HTTPException(status_code=400, detail="メールアドレスが既に存在します")

    # 更新
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    return user


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int = Path(..., ge=1, description="ユーザーID")
):
    """ユーザー削除"""
    global users_db

    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    users_db = [u for u in users_db if u.id != user_id]

    return {"message": "ユーザーを削除しました"}

# --- 学習用エンドポイント ---


@app.get("/examples/query-params")
async def query_params_example(
    required_param: str,
    optional_param: Optional[str] = None,
    default_param: str = "デフォルト値",
    int_param: int = Query(..., ge=0, le=100, description="0-100の整数"),
    list_param: List[str] = Query([], description="文字列のリスト")
):
    """クエリパラメータの例"""
    return {
        "required_param": required_param,
        "optional_param": optional_param,
        "default_param": default_param,
        "int_param": int_param,
        "list_param": list_param
    }


@app.get("/examples/path-params/{item_id}")
async def path_params_example(
    item_id: int = Path(..., ge=1, description="アイテムID"),
    category: str = Path(..., pattern=r'^[a-z]+$', description="カテゴリ（小文字のみ）")
):
    """パスパラメータの例"""
    return {
        "item_id": item_id,
        "category": category,
        "message": f"アイテム{item_id}（カテゴリ：{category}）"
    }


class ExampleRequest(BaseModel):
    """リクエストボディの例"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    priority: int = Field(1, ge=1, le=5)


@app.post("/examples/request-body")
async def request_body_example(request: ExampleRequest):
    """リクエストボディの例"""
    return {
        "received_data": request.model_dump(),
        "message": "データを受信しました"
    }

# --- 実行用の設定 ---

if __name__ == "__main__":
    import uvicorn

    print("🚀 FastAPI基礎学習サーバーを起動中...")
    print("📖 API文書: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("🔧 サーバー停止: Ctrl+C")

    uvicorn.run(
        "fastapi_hello_world:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["./"]
    )
