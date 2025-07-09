from fastapi import FastAPI

# --- FastAPIアプリケーションの作成 ---
app = FastAPI(
    title="Todo API",
    description="TODOアプリケーションのAPI",
    version="1.0.0"
)

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