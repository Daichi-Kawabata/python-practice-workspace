"""
View層 - Task関連のレスポンス形式
MVCパターンにおけるView層の実装例

役割:
- APIレスポンスの形式定義
- データの表示方法の決定
- エラーレスポンスの形式統一
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class Priority(str, Enum):
    """タスクの優先度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBaseView(BaseModel):
    """
    タスクの基本ビュー

    MVCのView層の役割:
    - データの表示形式を定義
    - APIレスポンスの構造を決定
    """
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TaskCreateView(TaskBaseView):
    """
    タスク作成時のリクエスト/レスポンス形式

    View層の責任:
    - 入力データの形式定義
    - バリデーションルールの設定
    """
    pass


class TaskUpdateView(BaseModel):
    """
    タスク更新時のリクエスト形式

    View層の特徴:
    - 部分更新のためのOptional項目
    - 更新可能な項目のみを定義
    """
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class TaskResponseView(TaskBaseView):
    """
    タスクレスポンスの形式

    View層の役割:
    - クライアントに返すデータの構造定義
    - 表示用の追加情報の提供
    """
    id: int
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    # 計算された値（表示用）
    is_overdue: bool = False

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_model(cls, task_model) -> "TaskResponseView":
        """
        モデルからビューを作成

        View層の責任:
        - モデルデータの表示形式への変換
        - 表示用データの追加
        """
        return cls(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            priority=task_model.priority,
            due_date=task_model.due_date,
            completed=task_model.completed,
            user_id=task_model.user_id,
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
            is_overdue=task_model.is_overdue()
        )


class TaskListResponseView(BaseModel):
    """
    タスクリストのレスポンス形式

    View層の役割:
    - リスト形式データの構造定義
    - ページネーション情報の提供
    - 統計情報の追加
    """
    tasks: List[TaskResponseView]
    total_count: int
    completed_count: int
    pending_count: int
    overdue_count: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_tasks(cls, tasks: List) -> "TaskListResponseView":
        """
        タスクリストからビューを作成

        View層の責任:
        - リストデータの整形
        - 統計情報の計算
        """
        task_views = [TaskResponseView.from_model(task) for task in tasks]

        return cls(
            tasks=task_views,
            total_count=len(tasks),
            completed_count=len([t for t in tasks if t.completed]),
            pending_count=len([t for t in tasks if not t.completed]),
            overdue_count=len([t for t in tasks if t.is_overdue()])
        )


class TaskStatsView(BaseModel):
    """
    タスク統計情報のビュー

    View層の役割:
    - 統計データの表示形式定義
    - ダッシュボード用データの提供
    """
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    completion_rate: float

    # 優先度別の統計
    high_priority_tasks: int
    medium_priority_tasks: int
    low_priority_tasks: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_tasks(cls, tasks: List) -> "TaskStatsView":
        """
        タスクリストから統計ビューを作成

        View層の責任:
        - 統計データの計算
        - パーセンテージなどの表示用データの生成
        """
        total = len(tasks)
        completed = len([t for t in tasks if t.completed])
        pending = len([t for t in tasks if not t.completed])
        overdue = len([t for t in tasks if t.is_overdue()])

        completion_rate = (completed / total * 100) if total > 0 else 0

        return cls(
            total_tasks=total,
            completed_tasks=completed,
            pending_tasks=pending,
            overdue_tasks=overdue,
            completion_rate=round(completion_rate, 2),
            high_priority_tasks=len(
                [t for t in tasks if t.priority == "high"]),
            medium_priority_tasks=len(
                [t for t in tasks if t.priority == "medium"]),
            low_priority_tasks=len([t for t in tasks if t.priority == "low"])
        )


class ErrorResponseView(BaseModel):
    """
    エラーレスポンスの形式

    View層の役割:
    - エラー情報の統一的な表示
    - クライアントフレンドリーなエラーメッセージ
    """
    error: str
    message: str
    code: int
    details: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SuccessResponseView(BaseModel):
    """
    成功レスポンスの形式

    View層の役割:
    - 成功時の統一的なレスポンス
    - 操作結果の明確な表示
    """
    success: bool = True
    message: str
    data: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


# ======= MVCパターンにおけるView層の特徴 =======

"""
1. データの表示形式定義
   - Pydanticモデルを使用したスキーマ定義
   - JSONレスポンスの構造決定

2. 表示用データの追加
   - 計算された値（is_overdue, completion_rate）
   - 統計情報の提供

3. エラーハンドリング
   - 統一的なエラーレスポンス形式
   - ユーザーフレンドリーなメッセージ

4. データ変換
   - モデルからビューへの変換メソッド
   - 表示用データの整形

5. 責任の分離
   - 表示ロジックのみを担当
   - ビジネスロジックは含まない
   - データベース操作は含まない

6. 再利用性
   - 複数のエンドポイントで使用可能
   - 一貫した表示形式の提供
"""
