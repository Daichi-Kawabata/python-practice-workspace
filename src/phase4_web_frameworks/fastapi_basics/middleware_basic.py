"""
FastAPI ミドルウェアの基本
========================

このファイルでは、FastAPIのミドルウェアについて学習します。
ミドルウェアは、リクエスト・レスポンスの処理を横断的に行う仕組みです。

- CORS（Cross-Origin Resource Sharing）
- ログ記録
- リクエスト時間測定
- カスタムヘッダー追加
- エラーハンドリング
"""

import time
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Dict, Any
import uuid

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI ミドルウェア基本", version="1.0.0")

# ===== 1. CORS ミドルウェア =====

# ミドルウェアは最後に追加したものが最初に実行され、順番にミドルウェアを処理していったあと、ビジネスロジックにを処理する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://localhost:8080"],  # 許可するオリジン
    allow_credentials=True,  # Cookieを含むリクエストを許可
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 許可するHTTPメソッド
    allow_headers=["*"],  # 許可するヘッダー
)

# ===== 2. 信頼できるホストのミドルウェア =====

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

# ===== 3. カスタムミドルウェア - リクエスト時間測定 =====


class TimingMiddleware(BaseHTTPMiddleware):
    """リクエスト処理時間を測定するミドルウェア"""

    async def dispatch(self, request: Request, call_next):
        # リクエスト開始時刻
        start_time = time.time()

        # レスポンス処理
        # call_nextは次のミドルウェアまたはエンドポイントを呼び出す
        response = await call_next(request)

        # 処理時間計算
        process_time = time.time() - start_time

        # レスポンスヘッダーに処理時間を追加
        response.headers["X-Process-Time"] = str(process_time)

        # ログ出力
        logger.info(
            f"{request.method} {request.url.path} - {process_time:.4f}s")

        return response


app.add_middleware(TimingMiddleware)

# ===== 4. ログ記録ミドルウェア =====


class LoggingMiddleware(BaseHTTPMiddleware):
    """詳細なリクエスト・レスポンスログを記録"""

    async def dispatch(self, request: Request, call_next):
        # リクエストID生成
        request_id = str(uuid.uuid4())[:8]

        # リクエスト情報ログ
        logger.info(f"[{request_id}] {request.method} {request.url}")
        logger.info(
            f"[{request_id}] Client: {request.client.host if request.client else 'Unknown'}")
        logger.info(
            f"[{request_id}] User-Agent: {request.headers.get('user-agent', 'Unknown')}")

        try:
            # レスポンス処理
            response = await call_next(request)

            # レスポンス情報ログ
            logger.info(f"[{request_id}] Status: {response.status_code}")

            # レスポンスヘッダーにリクエストIDを追加
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # エラーログ
            logger.error(f"[{request_id}] Error: {str(e)}")
            raise


app.add_middleware(LoggingMiddleware)

# ===== 5. セキュリティヘッダーミドルウェア =====


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """セキュリティ関連のHTTPヘッダーを追加"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # セキュリティヘッダーを追加
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


app.add_middleware(SecurityHeadersMiddleware)

# ===== 6. エラーハンドリングミドルウェア =====


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """グローバルエラーハンドリング"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException:
            # HTTPExceptionはそのまま再発生
            raise
        except Exception as e:
            # 予期しないエラーをログに記録
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)

            # 500エラーとして返す
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "予期しないエラーが発生しました。",
                    "type": type(e).__name__
                }
            )


app.add_middleware(ErrorHandlingMiddleware)

# ===== API エンドポイント =====


@app.get("/")
async def root() -> Dict[str, Any]:
    """ルートエンドポイント"""
    return {
        "message": "FastAPI ミドルウェア基本サンプル",
        "middleware_applied": [
            "CORS",
            "TrustedHost",
            "Timing",
            "Logging",
            "SecurityHeaders",
            "ErrorHandling"
        ],
        "note": "レスポンスヘッダーを確認してください"
    }


@app.get("/slow")
async def slow_endpoint():
    """処理時間測定用の遅いエンドポイント"""
    import asyncio
    await asyncio.sleep(2)  # 2秒待機

    return {
        "message": "2秒の処理が完了しました",
        "note": "X-Process-Timeヘッダーで処理時間を確認できます"
    }


@app.get("/error")
async def error_endpoint():
    """エラーハンドリング確認用"""
    raise Exception("テスト用の例外です")


@app.get("/http-error")
async def http_error_endpoint():
    """HTTPエラー確認用"""
    raise HTTPException(status_code=400, detail="テスト用のHTTPエラーです")


@app.get("/headers")
async def get_headers(request: Request):
    """リクエストヘッダー確認用"""
    return {
        "headers": dict(request.headers),
        "client": str(request.client),
        "method": request.method,
        "url": str(request.url)
    }


@app.post("/cors-test")
async def cors_test(data: Dict[str, Any]):
    """CORS動作確認用"""
    return {
        "message": "CORSテスト成功",
        "received_data": data,
        "note": "フロントエンドからのクロスオリジンリクエストが成功しました"
    }

# ===== ミドルウェアの動作確認方法 =====


@app.get("/middleware-info")
async def middleware_info():
    """ミドルウェアの動作確認方法"""
    return {
        "title": "ミドルウェア動作確認方法",
        "examples": [
            {
                "endpoint": "GET /",
                "description": "基本的なレスポンス確認",
                "check": "レスポンスヘッダーを確認"
            },
            {
                "endpoint": "GET /slow",
                "description": "処理時間測定",
                "check": "X-Process-Timeヘッダーの値"
            },
            {
                "endpoint": "GET /error",
                "description": "エラーハンドリング",
                "check": "500エラーのレスポンス形式"
            },
            {
                "endpoint": "GET /headers",
                "description": "リクエストヘッダー確認",
                "check": "X-Request-IDが追加されているか"
            }
        ],
        "browser_tools": [
            "開発者ツール > Network タブでヘッダー確認",
            "Postmanでリクエスト送信テスト",
            "curlコマンドでヘッダー確認: curl -v http://localhost:8000/"
        ]
    }

# ===== 実行例 =====

if __name__ == "__main__":
    import uvicorn

    print("FastAPI ミドルウェア基本サンプル")
    print("=" * 40)
    print("このサンプルでは以下のミドルウェアを学習します:")
    print("1. CORS - クロスオリジンリクエスト対応")
    print("2. TrustedHost - 信頼できるホストの制限")
    print("3. Timing - リクエスト処理時間測定")
    print("4. Logging - 詳細なログ記録")
    print("5. SecurityHeaders - セキュリティヘッダー追加")
    print("6. ErrorHandling - グローバルエラーハンドリング")
    print("\nサーバーを起動します...")
    print("ブラウザで http://localhost:8010/docs にアクセスして")
    print("各エンドポイントをテストしてください。")
    print("開発者ツール > Network タブでヘッダーも確認してください。")
    print("\nCtrl+C で停止")
    print("=" * 40)

    uvicorn.run(app, host="0.0.0.0", port=8010)
