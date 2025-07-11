from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, tasks
from .database import init_db

# --- FastAPIアプリケーションの作成 ---
app = FastAPI(
    title="Todo API",
    description="TODOアプリケーションのAPI",
    version="1.0.0"
)

# --- データベース初期化 ---
init_db()

# --- CORSミドルウェアの設定 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ルーターの登録 ---
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {"message": "Welcome to the Todo API!"}


@app.get("/health")
async def health():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}

# --- 実行設定 ---
if __name__ == "__main__":
    import uvicorn

    print("📖 API文書: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["./"]
    )
