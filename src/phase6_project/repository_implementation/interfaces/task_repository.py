"""
TaskRepositoryインターフェース

役割:
- タスクに関するデータアクセス操作の定義
- タスク固有の操作方法の抽象化
- 実装の詳細の隠蔽
"""

from abc import abstractmethod
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from .base_repository import BaseRepositoryWithUser

# 型のインポート（実際のプロジェクトでは適切なパスに変更）
from typing import TypeVar, Dict, Any

# 仮の型定義（実際のプロジェクトでは適切なインポートに変更）
Task = TypeVar('Task')
TaskCreate = TypeVar('TaskCreate')
TaskUpdate = TypeVar('TaskUpdate')


class TaskRepositoryInterface(BaseRepositoryWithUser[Task, TaskCreate, TaskUpdate]):
    """
    タスクリポジトリインターフェース

    タスクに関するデータアクセス操作を定義
    基底リポジトリのCRUD操作に加えて、タスク固有の操作を追加
    """

    # ====== タスク固有の検索メソッド ======

    @abstractmethod
    async def get_by_status(
        self,
        db: Session,
        user_id: int,
        completed: bool,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        完了状態によるタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            completed: 完了状態（True: 完了、False: 未完了）
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass

    @abstractmethod
    async def get_by_priority(
        self,
        db: Session,
        user_id: int,
        priority: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        優先度によるタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            priority: 優先度（low, medium, high）
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass

    @abstractmethod
    async def get_overdue_tasks(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        期限切れタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 期限切れタスクのリスト
        """
        pass

    @abstractmethod
    async def get_due_today(
        self,
        db: Session,
        user_id: int
    ) -> List[Task]:
        """
        今日期限のタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            List[Task]: 今日期限のタスクのリスト
        """
        pass

    @abstractmethod
    async def get_due_this_week(
        self,
        db: Session,
        user_id: int
    ) -> List[Task]:
        """
        今週期限のタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            List[Task]: 今週期限のタスクのリスト
        """
        pass

    # ====== タスクの一括操作 ======

    @abstractmethod
    async def mark_completed(
        self,
        db: Session,
        user_id: int,
        task_id: int
    ) -> Optional[Task]:
        """
        タスクを完了状態にする

        Args:
            db: データベースセッション
            user_id: ユーザーID
            task_id: タスクID

        Returns:
            Optional[Task]: 更新されたタスク（存在しない場合None）
        """
        pass

    @abstractmethod
    async def mark_incomplete(
        self,
        db: Session,
        user_id: int,
        task_id: int
    ) -> Optional[Task]:
        """
        タスクを未完了状態にする

        Args:
            db: データベースセッション
            user_id: ユーザーID
            task_id: タスクID

        Returns:
            Optional[Task]: 更新されたタスク（存在しない場合None）
        """
        pass

    @abstractmethod
    async def bulk_update_priority(
        self,
        db: Session,
        user_id: int,
        task_ids: List[int],
        priority: str
    ) -> List[Task]:
        """
        複数タスクの優先度を一括更新

        Args:
            db: データベースセッション
            user_id: ユーザーID
            task_ids: 更新対象のタスクIDリスト
            priority: 新しい優先度

        Returns:
            List[Task]: 更新されたタスクのリスト
        """
        pass

    @abstractmethod
    async def bulk_delete(
        self,
        db: Session,
        user_id: int,
        task_ids: List[int]
    ) -> int:
        """
        複数タスクの一括削除

        Args:
            db: データベースセッション
            user_id: ユーザーID
            task_ids: 削除対象のタスクIDリスト

        Returns:
            int: 削除されたタスクの数
        """
        pass

    # ====== 統計情報の取得 ======

    @abstractmethod
    async def get_task_stats(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, int]:
        """
        タスクの統計情報を取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Dict[str, int]: 統計情報
            {
                'total': 総タスク数,
                'completed': 完了タスク数,
                'pending': 未完了タスク数,
                'overdue': 期限切れタスク数,
                'high_priority': 高優先度タスク数,
                'medium_priority': 中優先度タスク数,
                'low_priority': 低優先度タスク数
            }
        """
        pass

    @abstractmethod
    async def get_completion_rate(
        self,
        db: Session,
        user_id: int
    ) -> float:
        """
        タスクの完了率を取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            float: 完了率（0.0 - 1.0）
        """
        pass

    # ====== 検索・フィルタリング ======

    @abstractmethod
    async def search_tasks(
        self,
        db: Session,
        user_id: int,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        タスクの検索（タイトル・説明で検索）

        Args:
            db: データベースセッション
            user_id: ユーザーID
            query: 検索クエリ
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 検索結果のタスクリスト
        """
        pass

    @abstractmethod
    async def get_tasks_with_filters(
        self,
        db: Session,
        user_id: int,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        複数条件によるタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            completed: 完了状態（Noneの場合は全て）
            priority: 優先度（Noneの場合は全て）
            due_date_from: 期限日の開始日
            due_date_to: 期限日の終了日
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 条件に一致するタスクのリスト
        """
        pass


# ======= タスクリポジトリインターフェースの特徴 =======

"""
1. ドメイン固有の操作
   - タスクに特化した検索・操作メソッド
   - ビジネスロジックに基づいた機能定義

2. 豊富な検索オプション
   - 完了状態、優先度、期限日による検索
   - 複合条件による柔軟な検索

3. 一括操作
   - 複数タスクの一括更新・削除
   - 効率的なデータ操作

4. 統計情報
   - タスクの統計データ取得
   - 完了率などの計算された値

5. 拡張性
   - 新しい検索条件の追加が容易
   - ビジネス要件の変更に対応可能

6. 抽象化
   - 具体的な実装（SQLAlchemy、MongoDB等）から独立
   - テスタビリティの向上
"""
