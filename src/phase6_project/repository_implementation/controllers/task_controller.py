"""
TaskController - Controller層の実装例

役割:
- HTTPリクエストの処理
- Service層の呼び出し
- HTTPレスポンスの構築
- エラーハンドリング
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from ..services.task_service import TaskService

# 仮の型定義（実際のプロジェクトでは適切なインポートに変更）
from typing import Any as Task
from typing import Any as TaskCreate
from typing import Any as TaskUpdate
from typing import Any as TaskResponse
from typing import Any as User

# 依存性注入のダミー（実際のプロジェクトでは適切に実装）


def get_db():
    """データベースセッションを取得"""
    return None  # type: ignore


def get_current_user():
    """現在のユーザーを取得"""
    return None  # type: ignore


def get_task_service() -> TaskService:
    """TaskServiceを取得"""
    return None  # type: ignore


class TaskController:
    """
    タスクコントローラー - Controller層

    責任:
    - HTTPリクエストの受信と処理
    - Service層メソッドの呼び出し
    - HTTPレスポンスの構築
    - エラーハンドリングとHTTPステータスコードの設定
    """

    def __init__(self):
        self.router = APIRouter(prefix="/tasks", tags=["tasks"])
        self._register_routes()

    def _register_routes(self):
        """ルートの登録"""
        self.router.post("/", response_model=TaskResponse)(self.create_task)
        self.router.get("/", response_model=List[TaskResponse])(self.get_tasks)
        self.router.get(
            "/{task_id}", response_model=TaskResponse)(self.get_task)
        self.router.put(
            "/{task_id}", response_model=TaskResponse)(self.update_task)
        self.router.delete("/{task_id}")(self.delete_task)
        self.router.post("/{task_id}/complete",
                         response_model=TaskResponse)(self.complete_task)
        self.router.post("/{task_id}/incomplete",
                         response_model=TaskResponse)(self.incomplete_task)
        self.router.get(
            "/search", response_model=List[TaskResponse])(self.search_tasks)
        self.router.get(
            "/statistics", response_model=Dict[str, Any])(self.get_statistics)
        self.router.get(
            "/insights", response_model=Dict[str, Any])(self.get_insights)

    # ====== 基本的なCRUD操作 ======

    async def create_task(
        self,
        task_data: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> TaskResponse:
        """
        タスク作成エンドポイント

        Args:
            task_data: タスク作成データ
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            TaskResponse: 作成されたタスク

        Raises:
            HTTPException: バリデーションエラー、ビジネスルール違反
        """
        try:
            # Service層のメソッドを呼び出し
            task = await task_service.create_task(
                db=db,
                task_data=task_data,
                user_id=current_user.id
            )
            return task
        except ValueError as e:
            # バリデーションエラー
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            # ビジネスルール違反
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            # その他のエラー
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def get_tasks(
        self,
        skip: int = Query(0, ge=0, description="スキップ件数"),
        limit: int = Query(100, ge=1, le=1000, description="取得件数上限"),
        completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
        priority: Optional[str] = Query(None, description="優先度でフィルタ"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> List[TaskResponse]:
        """
        タスク一覧取得エンドポイント

        Args:
            skip: スキップ件数
            limit: 取得件数上限
            completed: 完了状態でのフィルタ
            priority: 優先度でのフィルタ
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            List[TaskResponse]: タスクのリスト
        """
        try:
            # フィルタ条件を構築
            filters = {}
            if completed is not None:
                filters['completed'] = completed
            if priority is not None:
                filters['priority'] = priority

            # Service層のメソッドを呼び出し
            tasks = await task_service.get_user_tasks(
                db=db,
                user_id=current_user.id,
                filters=filters,
                skip=skip,
                limit=limit
            )
            return tasks
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def get_task(
        self,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> TaskResponse:
        """
        タスク詳細取得エンドポイント

        Args:
            task_id: タスクID
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            TaskResponse: タスクの詳細

        Raises:
            HTTPException: タスクが見つからない場合
        """
        try:
            task = await task_service.get_task_by_id(
                db=db,
                task_id=task_id,
                user_id=current_user.id
            )

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            return task
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> TaskResponse:
        """
        タスク更新エンドポイント

        Args:
            task_id: タスクID
            task_data: タスク更新データ
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            TaskResponse: 更新されたタスク

        Raises:
            HTTPException: バリデーションエラー、権限エラー、タスクが見つからない場合
        """
        try:
            task = await task_service.update_task(
                db=db,
                task_id=task_id,
                task_data=task_data,
                user_id=current_user.id
            )

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def delete_task(
        self,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> Dict[str, str]:
        """
        タスク削除エンドポイント

        Args:
            task_id: タスクID
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            Dict[str, str]: 削除完了メッセージ

        Raises:
            HTTPException: 権限エラー、タスクが見つからない場合
        """
        try:
            success = await task_service.delete_task(
                db=db,
                task_id=task_id,
                user_id=current_user.id
            )

            if not success:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            return {"message": "タスクを削除しました"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    # ====== タスク状態操作 ======

    async def complete_task(
        self,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> TaskResponse:
        """
        タスク完了エンドポイント

        Args:
            task_id: タスクID
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            TaskResponse: 完了されたタスク
        """
        try:
            task = await task_service.complete_task(
                db=db,
                task_id=task_id,
                user_id=current_user.id
            )

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def incomplete_task(
        self,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> TaskResponse:
        """
        タスク未完了エンドポイント

        Args:
            task_id: タスクID
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            TaskResponse: 未完了に戻されたタスク
        """
        try:
            task = await task_service.uncomplete_task(
                db=db,
                task_id=task_id,
                user_id=current_user.id
            )

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    # ====== 検索・統計機能 ======

    async def search_tasks(
        self,
        query: str = Query(..., description="検索クエリ"),
        skip: int = Query(0, ge=0, description="スキップ件数"),
        limit: int = Query(100, ge=1, le=1000, description="取得件数上限"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> List[TaskResponse]:
        """
        タスク検索エンドポイント

        Args:
            query: 検索クエリ
            skip: スキップ件数
            limit: 取得件数上限
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            List[TaskResponse]: 検索結果のタスクリスト
        """
        try:
            tasks = await task_service.search_tasks(
                db=db,
                user_id=current_user.id,
                query=query,
                skip=skip,
                limit=limit
            )
            return tasks
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def get_statistics(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> Dict[str, Any]:
        """
        タスク統計情報取得エンドポイント

        Args:
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            Dict[str, Any]: 統計情報
        """
        try:
            stats = await task_service.get_task_statistics(
                db=db,
                user_id=current_user.id
            )
            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")

    async def get_insights(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        task_service: TaskService = Depends(get_task_service)
    ) -> Dict[str, Any]:
        """
        生産性インサイト取得エンドポイント

        Args:
            db: データベースセッション
            current_user: 現在のユーザー
            task_service: タスクサービス

        Returns:
            Dict[str, Any]: 生産性インサイト
        """
        try:
            insights = await task_service.get_productivity_insights(
                db=db,
                user_id=current_user.id
            )
            return insights
        except Exception as e:
            raise HTTPException(status_code=500, detail="内部サーバーエラー")


# ======= Controller層の特徴 =======

"""
1. HTTP処理の専門化
   - HTTPリクエストの受信と処理
   - HTTPレスポンスの構築
   - 適切なHTTPステータスコードの設定

2. Service層との協調
   - ビジネスロジックはService層に委譲
   - 複雑な処理はService層のメソッドを呼び出し

3. エラーハンドリング
   - 例外をHTTPエラーに変換
   - クライアントに適切なエラーメッセージを返却

4. 依存性注入
   - 必要なサービスを依存性注入で取得
   - テスタビリティとメンテナンス性を向上

5. バリデーション
   - リクエストデータの基本的なバリデーション
   - 詳細なビジネスルールの検証はService層で実施

6. ルーティング
   - URLパスとHTTPメソッドの定義
   - 適切なエンドポイントの設計

7. ドキュメンテーション
   - OpenAPIスキーマの自動生成
   - APIドキュメントの提供
"""
