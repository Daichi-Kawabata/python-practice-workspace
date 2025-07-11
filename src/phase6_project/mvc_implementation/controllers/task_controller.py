"""
Controller層 - Task関連のコントローラー
MVCパターンにおけるController層の実装例

役割:
- HTTPリクエストの処理
- モデルとビューの調整
- 認証・認可の処理
- エラーハンドリング
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

# 仮のインポート（実際のプロジェクトでは適切なパスに変更）
from ..models.task import Task
from ..models.user import User
from ..views.task_views import (
    TaskCreateView, TaskUpdateView, TaskResponseView,
    TaskListResponseView, TaskStatsView, ErrorResponseView
)

# 仮の依存関数（実際のプロジェクトでは適切に実装）


def get_db_session():
    """データベースセッションの取得"""
    # 実際の実装では、データベースセッションを返す
    pass


def get_current_user():
    """現在のユーザーの取得"""
    # 実際の実装では、認証されたユーザーを返す
    pass


# ルーター作成
router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskController:
    """
    TaskController - MVCのController層

    責任:
    - HTTPリクエストの処理
    - モデルとビューの調整
    - ビジネスロジックの呼び出し
    - レスポンスの構築
    """

    @staticmethod
    @router.post("/", response_model=TaskResponseView)
    async def create_task(
        task_data: TaskCreateView,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスク作成エンドポイント

        Controller層の責任:
        - リクエストデータの受信
        - モデルの呼び出し
        - ビューの構築
        """
        try:
            # 1. データの検証（View層で基本検証、Controller層で追加検証）
            Task.validate_task_data(task_data.title, task_data.priority)

            # 2. モデルの作成（Model層の責任）
            new_task = Task(
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                due_date=task_data.due_date,
                user_id=current_user.id
            )

            # 3. データベースへの保存
            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            # 4. レスポンスの構築（View層の責任）
            return TaskResponseView.from_model(new_task)

        except ValueError as e:
            # Controller層でのエラーハンドリング
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # 予期しないエラーの処理
            raise HTTPException(status_code=500, detail="タスクの作成に失敗しました")

    @staticmethod
    @router.get("/", response_model=TaskListResponseView)
    async def get_tasks(
        completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
        priority: Optional[str] = Query(None, description="優先度でフィルタ"),
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスクリスト取得エンドポイント

        Controller層の責任:
        - クエリパラメータの処理
        - フィルタリング条件の構築
        - モデルからのデータ取得
        """
        try:
            # 1. 基本クエリの構築
            query = db.query(Task).filter(Task.user_id == current_user.id)

            # 2. フィルタリング条件の適用
            if completed is not None:
                query = query.filter(Task.completed == completed)

            if priority:
                query = query.filter(Task.priority == priority)

            # 3. データの取得
            tasks = query.order_by(Task.created_at.desc()).all()

            # 4. レスポンスの構築
            return TaskListResponseView.from_tasks(tasks)

        except Exception as e:
            raise HTTPException(status_code=500, detail="タスクの取得に失敗しました")

    @staticmethod
    @router.get("/{task_id}", response_model=TaskResponseView)
    async def get_task(
        task_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        単一タスク取得エンドポイント

        Controller層の責任:
        - パスパラメータの処理
        - 権限チェック
        - 存在チェック
        """
        try:
            # 1. タスクの取得
            task = db.query(Task).filter(
                Task.id == task_id,
                Task.user_id == current_user.id
            ).first()

            # 2. 存在チェック
            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            # 3. レスポンスの構築
            return TaskResponseView.from_model(task)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="タスクの取得に失敗しました")

    @staticmethod
    @router.put("/{task_id}", response_model=TaskResponseView)
    async def update_task(
        task_id: int,
        task_data: TaskUpdateView,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスク更新エンドポイント

        Controller層の責任:
        - 更新データの処理
        - 部分更新の制御
        - 権限チェック
        """
        try:
            # 1. タスクの取得
            task = db.query(Task).filter(
                Task.id == task_id,
                Task.user_id == current_user.id
            ).first()

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            # 2. 更新データの適用
            update_data = task_data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if field == "priority" and value:
                    # Model層のビジネスロジックを使用
                    task.update_priority(value)
                elif field == "due_date":
                    # Model層のビジネスロジックを使用
                    task.set_due_date(value)
                elif field == "completed":
                    # Model層のビジネスロジックを使用
                    if value:
                        task.mark_completed()
                    else:
                        task.mark_incomplete()
                else:
                    # その他の項目は直接更新
                    setattr(task, field, value)

            # 3. データベースへの保存
            db.commit()
            db.refresh(task)

            # 4. レスポンスの構築
            return TaskResponseView.from_model(task)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="タスクの更新に失敗しました")

    @staticmethod
    @router.delete("/{task_id}")
    async def delete_task(
        task_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスク削除エンドポイント

        Controller層の責任:
        - 削除権限の確認
        - 削除処理の実行
        - 削除結果の返却
        """
        try:
            # 1. タスクの取得
            task = db.query(Task).filter(
                Task.id == task_id,
                Task.user_id == current_user.id
            ).first()

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            # 2. 削除処理
            db.delete(task)
            db.commit()

            # 3. 成功レスポンス
            return {"message": "タスクが削除されました"}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="タスクの削除に失敗しました")

    @staticmethod
    @router.get("/stats/summary", response_model=TaskStatsView)
    async def get_task_stats(
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスク統計取得エンドポイント

        Controller層の責任:
        - 統計データの取得
        - View層での統計計算の呼び出し
        """
        try:
            # 1. ユーザーのタスク取得
            tasks = db.query(Task).filter(
                Task.user_id == current_user.id).all()

            # 2. 統計データの構築（View層の責任）
            return TaskStatsView.from_tasks(tasks)

        except Exception as e:
            raise HTTPException(status_code=500, detail="統計データの取得に失敗しました")

    @staticmethod
    @router.patch("/{task_id}/complete")
    async def complete_task(
        task_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
    ):
        """
        タスク完了マークエンドポイント

        Controller層の責任:
        - 特定のアクションの処理
        - Model層のビジネスロジック呼び出し
        """
        try:
            # 1. タスクの取得
            task = db.query(Task).filter(
                Task.id == task_id,
                Task.user_id == current_user.id
            ).first()

            if not task:
                raise HTTPException(status_code=404, detail="タスクが見つかりません")

            # 2. Model層のビジネスロジック呼び出し
            task.mark_completed()

            # 3. データベースへの保存
            db.commit()

            # 4. レスポンス
            return {"message": "タスクが完了しました"}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="タスクの完了に失敗しました")


# ======= MVCパターンにおけるController層の特徴 =======

"""
1. HTTPリクエストの処理
   - FastAPIのエンドポイント定義
   - パスパラメータ、クエリパラメータの処理
   - リクエストボディの受信

2. 認証・認可
   - ユーザー認証の確認
   - アクセス権限のチェック
   - セキュリティ制御

3. モデルとビューの調整
   - Model層のビジネスロジック呼び出し
   - View層のレスポンス構築
   - データの変換・整形

4. エラーハンドリング
   - 例外の捕捉と処理
   - 適切なHTTPステータスコードの設定
   - エラーメッセージの構築

5. 責任の分離
   - ビジネスロジックはModel層に委譲
   - 表示ロジックはView層に委譲
   - HTTPに関する処理のみを担当

6. 依存性の管理
   - 依存性注入の活用
   - 外部サービスとの連携
   - データベースセッションの管理
"""
