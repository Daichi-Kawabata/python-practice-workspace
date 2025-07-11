"""
FastAPIアプリケーションの統合例

役割:
- アプリケーションの初期化
- 依存性注入の設定
- ルーターの登録
- ミドルウェアの設定
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from .controllers.task_controller import TaskController
from .services.task_service import TaskService
from .implementations.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from .implementations.mock_repositories import MockTaskRepository
from .interfaces.task_repository import TaskRepositoryInterface
from .interfaces.user_repository import UserRepositoryInterface

# 仮の型定義
from typing import Any as User


class AppConfig:
    """アプリケーション設定"""
    USE_MOCK_DATA = True  # 開発時はTrue、本番時はFalse
    DATABASE_URL = "sqlite:///./test.db"


# グローバル変数（実際のプロジェクトでは適切なDIコンテナを使用）
app_config = AppConfig()


def get_database():
    """データベースセッションを取得"""
    # 実際のプロジェクトではSQLAlchemyのSessionLocalを使用
    return None


def get_current_user(db: Session = Depends(get_database)) -> User:
    """現在のユーザーを取得"""
    # 実際のプロジェクトではJWTトークンから取得
    return None


def get_task_repository() -> TaskRepositoryInterface:
    """タスクリポジトリを取得"""
    if app_config.USE_MOCK_DATA:
        return MockTaskRepository()
    else:
        # 実際のプロジェクトでは適切なモデルクラスを渡す
        return SQLAlchemyTaskRepository(model_class=None)


def get_user_repository() -> UserRepositoryInterface:
    """ユーザーリポジトリを取得"""
    # 実際のプロジェクトでは適切な実装を返す
    return None  # type: ignore


def get_task_service(
    task_repository: TaskRepositoryInterface = Depends(get_task_repository),
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> TaskService:
    """タスクサービスを取得"""
    return TaskService(task_repository, user_repository)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    print("アプリケーションを起動中...")
    yield
    # 終了時の処理
    print("アプリケーションを終了中...")


def create_app() -> FastAPI:
    """FastAPIアプリケーションを作成"""

    # FastAPIアプリケーションの初期化
    app = FastAPI(
        title="Task Management API",
        description="Repositoryパターンを使用したタスク管理API",
        version="1.0.0",
        lifespan=lifespan
    )

    # コントローラーの初期化
    task_controller = TaskController()

    # 依存性注入の設定（実際のプロジェクトでは別ファイルで管理）
    task_controller.router.dependencies.extend([
        Depends(get_database),
        Depends(get_current_user),
        Depends(get_task_service)
    ])

    # ルーターの登録
    app.include_router(task_controller.router)

    # ミドルウェアの設定
    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        """処理時間をヘッダーに追加"""
        import time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # グローバル例外ハンドラー
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """グローバル例外ハンドラー"""
        return {
            "error": "内部サーバーエラー",
            "message": "予期しないエラーが発生しました"
        }

    # ヘルスチェックエンドポイント
    @app.get("/health")
    async def health_check():
        """ヘルスチェック"""
        return {"status": "healthy"}

    return app


# アプリケーションインスタンス
app = create_app()


# ======= FastAPIアプリケーション統合の特徴 =======

"""
1. 依存性注入の設定
   - get_task_repository(): リポジトリの実装を切り替え可能
   - get_task_service(): サービスの依存関係を解決
   - get_current_user(): 認証・認可の処理

2. 設定管理
   - AppConfig: アプリケーションの設定を一元管理
   - 開発/本番環境での切り替えが容易

3. ライフサイクル管理
   - アプリケーションの起動・終了処理
   - リソースの初期化と解放

4. ミドルウェア
   - 横断的な処理の実装
   - ログ出力、認証、CORS設定など

5. エラーハンドリング
   - グローバル例外ハンドラー
   - 一貫したエラーレスポンス

6. ドキュメント生成
   - OpenAPIスキーマの自動生成
   - Swagger UIの提供

7. テスタビリティ
   - 依存性注入によるモック化
   - 統合テストの容易さ
"""


# ======= 使用例 =======

"""
# 開発時（モックデータ使用）
app_config.USE_MOCK_DATA = True
app = create_app()

# 本番時（実際のデータベース使用）
app_config.USE_MOCK_DATA = False
app = create_app()

# サーバー起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
