#!/usr/bin/env python3
"""
マルチステージビルド用の軽量FastAPIアプリケーション

本番環境での運用を想定した最適化されたアプリケーション
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import logging
import sys
from datetime import datetime
import uvicorn

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境変数から設定を取得
APP_NAME = os.getenv("APP_NAME", "Multi-stage FastAPI App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# FastAPIアプリケーション作成
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    description="マルチステージビルドで最適化されたFastAPIアプリケーション"
)

# データモデル


class HealthCheck(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str
    timestamp: datetime
    version: str
    build_info: Dict[str, Any]


class SystemInfo(BaseModel):
    """システム情報"""
    python_version: str
    platform: str
    environment: str
    memory_usage: str
    uptime: str


# グローバル変数
start_time = datetime.now()


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": f"Welcome to {APP_NAME}!",
        "version": APP_VERSION,
        "environment": "production" if not DEBUG else "development",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """アプリケーションのヘルスチェック"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version=APP_VERSION,
        build_info={
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "debug_mode": DEBUG,
            "uptime_seconds": (datetime.now() - start_time).total_seconds()
        }
    )


@app.get("/system", response_model=SystemInfo)
async def system_info():
    """システム情報を取得"""
    uptime = datetime.now() - start_time

    return SystemInfo(
        python_version=sys.version.split()[0],
        platform=sys.platform,
        environment="production" if not DEBUG else "development",
        memory_usage="N/A",  # 本番環境では詳細なメモリ情報は表示しない
        uptime=str(uptime).split('.')[0]  # 秒以下を切り捨て
    )


@app.get("/metrics")
async def metrics():
    """アプリケーションメトリクス"""
    uptime = (datetime.now() - start_time).total_seconds()

    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "uptime_seconds": uptime,
        "status": "running",
        "endpoints": [
            {"path": "/", "method": "GET"},
            {"path": "/health", "method": "GET"},
            {"path": "/system", "method": "GET"},
            {"path": "/metrics", "method": "GET"},
        ]
    }

# エラーハンドリング


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """グローバル例外ハンドラー"""
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )

# 起動時処理


@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Python version: {sys.version.split()[0]}")
    logger.info(f"Platform: {sys.platform}")


@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    uptime = datetime.now() - start_time
    logger.info(f"Shutting down {APP_NAME} after {uptime}")

if __name__ == "__main__":
    # 環境変数から設定を取得
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()

    logger.info(f"Starting server on {host}:{port}")

    # 本番環境用の設定
    uvicorn_config = {
        "app": "app:app",
        "host": host,
        "port": port,
        "log_level": log_level,
        "access_log": DEBUG,  # 本番では無効化
        "reload": False,      # 本番では無効化
        "workers": 1 if DEBUG else 4  # 本番では複数ワーカー
    }

    # サーバー起動
    uvicorn.run(**uvicorn_config)
