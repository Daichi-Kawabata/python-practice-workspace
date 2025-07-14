"""
FastAPI アプリケーションの実装例

設定管理を使用した実際のFastAPIアプリケーションの例
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime

# カスタム設定をインポート
from config import AppSettings, get_settings

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# セキュリティ
security = HTTPBearer()

# Pydanticモデル


class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    debug: bool
    version: str

# FastAPIアプリケーション作成関数


def create_app(settings: Optional[AppSettings] = None) -> FastAPI:
    """設定を使用してFastAPIアプリケーションを作成"""

    if settings is None:
        settings = get_settings()

    # ログレベルの設定
    log_level = getattr(logging, settings.log_level.upper())
    logger.setLevel(log_level)

    # FastAPIアプリケーションの初期化
    app = FastAPI(
        title=settings.name,
        version=settings.version,
        debug=settings.debug,
        description="設定管理を使用したFastAPIアプリケーション"
    )

    # CORS設定
    if settings.security.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.security.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # ミドルウェアでログ出力
    @app.middleware("http")
    async def log_requests(request, call_next):
        start_time = datetime.now()

        # リクエストをログ出力
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        # レスポンス時間を計算
        process_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")

        return response

    # ヘルスチェックエンドポイント
    @app.get("/health", response_model=HealthCheck)
    async def health_check(settings: AppSettings = Depends(get_settings)):
        """アプリケーションのヘルスチェック"""
        return HealthCheck(
            status="healthy",
            timestamp=datetime.now(),
            environment=settings.environment,
            debug=settings.debug,
            version=settings.version
        )

    # 設定表示エンドポイント（開発環境のみ）
    @app.get("/settings")
    async def get_app_settings(settings: AppSettings = Depends(get_settings)):
        """設定情報を取得（開発環境のみ）"""
        if settings.environment == "production":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Settings endpoint not available in production"
            )

        # 機密情報を隠した設定を返す
        return {
            "app_name": settings.name,
            "version": settings.version,
            "environment": settings.environment,
            "debug": settings.debug,
            "log_level": settings.log_level,
            "database_url": "***" if "password" in settings.database.url else settings.database.url,
            "redis_url": settings.redis.url,
            "allowed_hosts": settings.security.allowed_hosts,
            "cors_origins": settings.security.cors_origins,
        }

    # 認証が必要なエンドポイント（デモ用）
    @app.get("/protected")
    async def protected_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        settings: AppSettings = Depends(get_settings)
    ):
        """認証が必要な保護されたエンドポイント"""
        # 実際の実装では、JWTトークンを検証する
        if credentials.credentials == "demo-token":
            return {
                "message": "Access granted",
                "user": "demo-user",
                "timestamp": datetime.now()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    # ユーザー関連エンドポイント
    @app.post("/users", response_model=UserResponse)
    async def create_user(
        user: UserCreate,
        settings: AppSettings = Depends(get_settings)
    ):
        """ユーザーを作成（デモ用）"""
        # 実際の実装では、データベースに保存する
        logger.info(f"Creating user: {user.username}")

        return UserResponse(
            id=1,
            username=user.username,
            email=user.email,
            created_at=datetime.now()
        )

    @app.get("/users", response_model=List[UserResponse])
    async def get_users(
        limit: int = 10,
        settings: AppSettings = Depends(get_settings)
    ):
        """ユーザーリストを取得（デモ用）"""
        logger.info(f"Getting users with limit: {limit}")

        # デモデータを返す
        return [
            UserResponse(
                id=1,
                username="demo-user",
                email="demo@example.com",
                created_at=datetime.now()
            )
        ]

    # 環境固有の機能
    if settings.debug:
        @app.get("/debug")
        async def debug_info(settings: AppSettings = Depends(get_settings)):
            """デバッグ情報（デバッグモードのみ）"""
            return {
                "message": "Debug mode is enabled",
                "settings": {
                    "environment": settings.environment,
                    "log_level": settings.log_level,
                    "database_echo": settings.database.echo,
                },
                "timestamp": datetime.now()
            }

    return app


# アプリケーションインスタンス
app = create_app()

if __name__ == "__main__":
    import uvicorn

    # 設定を取得
    settings = get_settings()

    print("=" * 60)
    print("FastAPIアプリケーション起動")
    print("=" * 60)
    print(f"📱 アプリケーション: {settings.name}")
    print(f"🔢 バージョン: {settings.version}")
    print(f"🌍 環境: {settings.environment}")
    print(f"🐛 デバッグ: {settings.debug}")
    print(f"📊 ログレベル: {settings.log_level}")
    print("=" * 60)

    # 開発サーバーを起動
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
