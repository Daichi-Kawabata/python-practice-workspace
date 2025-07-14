#!/usr/bin/env python3
"""
FastAPI Docker Example

コンテナ化されたFastAPIアプリケーション
ヘルスチェック、環境変数管理、ログ設定を含む
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
import logging
import asyncio
from datetime import datetime
import uvicorn

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境変数から設定を取得
APP_NAME = os.getenv("APP_NAME", "FastAPI Docker App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# FastAPIアプリケーション作成
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    description="Docker化されたFastAPIアプリケーション"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル


class HealthCheck(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str
    timestamp: datetime
    version: str
    environment: Dict[str, Any]


class Item(BaseModel):
    """アイテムモデル"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None


class ItemResponse(BaseModel):
    """アイテムレスポンス"""
    success: bool
    data: Optional[Item] = None
    message: str


# インメモリデータストア（実際の実装ではDBを使用）
items_store: List[Item] = []
next_id = 1


def get_next_id():
    """次のIDを取得"""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

# ルートエンドポイント


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": f"Welcome to {APP_NAME}!",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

# ヘルスチェックエンドポイント


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """アプリケーションのヘルスチェック"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version=APP_VERSION,
        environment={
            "app_name": APP_NAME,
            "debug": DEBUG,
            "python_version": sys.version.split()[0],
            "items_count": len(items_store)
        }
    )

# アイテム関連エンドポイント


@app.get("/items", response_model=List[Item])
async def get_items(limit: int = 10):
    """アイテム一覧を取得"""
    logger.info(f"Fetching items with limit: {limit}")
    return items_store[:limit]


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """特定のアイテムを取得"""
    logger.info(f"Fetching item with ID: {item_id}")

    item = next((item for item in items_store if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemResponse(
        success=True,
        data=item,
        message="Item retrieved successfully"
    )


@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    """新しいアイテムを作成"""
    logger.info(f"Creating new item: {item.name}")

    # IDと作成日時を設定
    item.id = get_next_id()
    item.created_at = datetime.now()

    # ストアに追加
    items_store.append(item)

    return ItemResponse(
        success=True,
        data=item,
        message="Item created successfully"
    )


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, updated_item: Item):
    """アイテムを更新"""
    logger.info(f"Updating item with ID: {item_id}")

    # 既存アイテムを検索
    for i, item in enumerate(items_store):
        if item.id == item_id:
            # IDと作成日時は保持
            updated_item.id = item_id
            updated_item.created_at = item.created_at
            items_store[i] = updated_item

            return ItemResponse(
                success=True,
                data=updated_item,
                message="Item updated successfully"
            )

    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int):
    """アイテムを削除"""
    logger.info(f"Deleting item with ID: {item_id}")

    for i, item in enumerate(items_store):
        if item.id == item_id:
            deleted_item = items_store.pop(i)
            return ItemResponse(
                success=True,
                data=deleted_item,
                message="Item deleted successfully"
            )

    raise HTTPException(status_code=404, detail="Item not found")

# デバッグ用エンドポイント（開発環境のみ）
if DEBUG:
    @app.get("/debug/env")
    async def debug_environment():
        """環境変数を表示（デバッグ用）"""
        return {
            "environment_variables": {
                key: value for key, value in os.environ.items()
                if not key.startswith(('AWS_', 'SECRET_', 'PASSWORD'))
            }
        }

    @app.get("/debug/reset")
    async def debug_reset():
        """ストアをリセット（デバッグ用）"""
        global items_store, next_id
        items_store.clear()
        next_id = 1
        return {"message": "Store reset successfully"}

# 起動時処理


@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"CORS origins: {CORS_ORIGINS}")

    # サンプルデータを追加（デバッグモードの場合）
    if DEBUG:
        sample_items = [
            Item(name="Sample Item 1",
                 description="This is a sample item", price=100.0),
            Item(name="Sample Item 2",
                 description="Another sample item", price=200.0),
        ]

        for item in sample_items:
            item.id = get_next_id()
            item.created_at = datetime.now()
            items_store.append(item)

        logger.info(f"Added {len(sample_items)} sample items")


@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info(f"Shutting down {APP_NAME}")

if __name__ == "__main__":
    # 環境変数から設定を取得
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()

    logger.info(f"Starting server on {host}:{port}")

    # サーバー起動
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=DEBUG
    )
