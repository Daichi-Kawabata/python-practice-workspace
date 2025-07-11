"""
TaskService - ビジネスロジック層

役割:
- タスクに関するビジネスロジックの実装
- 複数のリポジトリを組み合わせた処理
- トランザクション管理
- バリデーション
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..interfaces.task_repository import TaskRepositoryInterface
from ..interfaces.user_repository import UserRepositoryInterface

# 仮の型定義（実際のプロジェクトでは適切なインポートに変更）
from typing import TypeVar, Any

# 実際の型の代わりに Any を使用（学習用サンプルのため）。
# 実際はPydanticスキーマが使用される想定
Task = Any
TaskCreate = Any
TaskUpdate = Any
User = Any


class TaskService:
    """
    タスクサービス - ビジネスロジック層

    責任:
    - タスクに関するビジネスルールの実装
    - 複数のリポジトリとの連携
    - トランザクション管理
    - データの整合性保証
    """

    def __init__(
        self,
        task_repository: TaskRepositoryInterface,
        user_repository: Optional[UserRepositoryInterface] = None
    ):
        """
        コンストラクタ

        Args:
            task_repository: タスクリポジトリ
            user_repository: ユーザーリポジトリ（オプション）
        """
        self.task_repository = task_repository
        self.user_repository = user_repository

    # ====== タスクの作成・更新 ======

    async def create_task(
        self,
        db: Session,
        task_data: TaskCreate,
        user_id: int
    ) -> Task:
        """
        タスクの作成

        Args:
            db: データベースセッション
            task_data: タスク作成データ
            user_id: ユーザーID

        Returns:
            Task: 作成されたタスク

        Raises:
            ValueError: バリデーションエラー
            RuntimeError: ビジネスルール違反
        """
        # 1. バリデーション
        await self._validate_task_data(task_data)

        # 2. ユーザーの存在確認
        if self.user_repository:
            user = await self.user_repository.get(db, user_id)
            if not user:
                raise ValueError("ユーザーが見つかりません")

        # 3. ビジネスルールチェック
        await self._check_task_creation_rules(db, user_id, task_data)

        # 4. タスクの作成
        # task_dataにuser_idを追加
        if hasattr(task_data, '__dict__'):
            task_data_dict = task_data.__dict__.copy()
        else:
            task_data_dict = dict(task_data) if hasattr(
                task_data, 'keys') else {}

        task_data_dict['user_id'] = user_id

        return await self.task_repository.create(db, task_data_dict)

    async def update_task(
        self,
        db: Session,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int
    ) -> Optional[Task]:
        """
        タスクの更新

        Args:
            db: データベースセッション
            task_id: タスクID
            task_data: タスク更新データ
            user_id: ユーザーID

        Returns:
            Optional[Task]: 更新されたタスク（存在しない場合None）

        Raises:
            ValueError: バリデーションエラー
            PermissionError: アクセス権限エラー
        """
        # 1. 既存タスクの取得
        existing_task = await self.task_repository.get_by_user_and_id(db, user_id, task_id)
        if not existing_task:
            raise ValueError("タスクが見つかりません")

        # 2. バリデーション
        await self._validate_task_update_data(task_data, existing_task)

        # 3. ビジネスルールチェック
        await self._check_task_update_rules(db, existing_task, task_data)

        # 4. タスクの更新
        return await self.task_repository.update(db, existing_task, task_data)

    async def delete_task(
        self,
        db: Session,
        task_id: int,
        user_id: int
    ) -> bool:
        """
        タスクの削除

        Args:
            db: データベースセッション
            task_id: タスクID
            user_id: ユーザーID

        Returns:
            bool: 削除成功時True、失敗時False

        Raises:
            PermissionError: アクセス権限エラー
        """
        # 1. 既存タスクの取得と権限チェック
        existing_task = await self.task_repository.get_by_user_and_id(db, user_id, task_id)
        if not existing_task:
            raise ValueError("タスクが見つかりません")

        # 2. 削除ルールチェック
        await self._check_task_deletion_rules(db, existing_task)

        # 3. タスクの削除
        return await self.task_repository.delete(db, task_id)

    # ====== タスクの取得・検索 ======

    async def get_user_tasks(
        self,
        db: Session,
        user_id: int,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        ユーザーのタスク一覧を取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            filters: フィルタリング条件
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: タスクのリスト
        """
        if not filters:
            filters = {}

        return await self.task_repository.get_by_user(
            db, user_id, skip, limit, **filters
        )

    async def get_task_by_id(
        self,
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[Task]:
        """
        タスクをIDで取得

        Args:
            db: データベースセッション
            task_id: タスクID
            user_id: ユーザーID

        Returns:
            Optional[Task]: 取得されたタスク（存在しない場合None）
        """
        return await self.task_repository.get_by_user_and_id(db, user_id, task_id)

    async def search_tasks(
        self,
        db: Session,
        user_id: int,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        タスクの検索

        Args:
            db: データベースセッション
            user_id: ユーザーID
            query: 検索クエリ
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[Task]: 検索結果のタスクリスト
        """
        # 検索クエリの前処理
        query = query.strip()
        if not query:
            return []

        return await self.task_repository.search_tasks(db, user_id, query, skip, limit)

    # ====== タスクの状態操作 ======

    async def complete_task(
        self,
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[Task]:
        """
        タスクを完了状態にする

        Args:
            db: データベースセッション
            task_id: タスクID
            user_id: ユーザーID

        Returns:
            Optional[Task]: 更新されたタスク（存在しない場合None）
        """
        # 1. タスクの取得
        task = await self.task_repository.get_by_user_and_id(db, user_id, task_id)
        if not task:
            raise ValueError("タスクが見つかりません")

        # 2. 完了ルールチェック
        await self._check_task_completion_rules(db, task)

        # 3. タスクを完了状態にする
        return await self.task_repository.mark_completed(db, user_id, task_id)

    async def uncomplete_task(
        self,
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[Task]:
        """
        タスクを未完了状態にする

        Args:
            db: データベースセッション
            task_id: タスクID
            user_id: ユーザーID

        Returns:
            Optional[Task]: 更新されたタスク（存在しない場合None）
        """
        # 1. タスクの取得
        task = await self.task_repository.get_by_user_and_id(db, user_id, task_id)
        if not task:
            raise ValueError("タスクが見つかりません")

        # 2. 未完了ルールチェック
        await self._check_task_incompletion_rules(db, task)

        # 3. タスクを未完了状態にする
        return await self.task_repository.mark_incomplete(db, user_id, task_id)

    async def bulk_update_priority(
        self,
        db: Session,
        task_ids: List[int],
        priority: str,
        user_id: int
    ) -> List[Task]:
        """
        複数タスクの優先度を一括更新

        Args:
            db: データベースセッション
            task_ids: タスクIDのリスト
            priority: 新しい優先度
            user_id: ユーザーID

        Returns:
            List[Task]: 更新されたタスクのリスト
        """
        # 1. 優先度の検証
        valid_priorities = ['low', 'medium', 'high']
        if priority not in valid_priorities:
            raise ValueError(f"優先度は {valid_priorities} のいずれかである必要があります")

        # 2. 一括更新の実行
        return await self.task_repository.bulk_update_priority(db, user_id, task_ids, priority)

    # ====== 統計・分析 ======

    async def get_task_statistics(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """
        タスクの統計情報を取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Dict[str, Any]: 統計情報
        """
        # 1. 基本統計の取得
        stats = await self.task_repository.get_task_stats(db, user_id)

        # 2. 完了率の計算
        completion_rate = await self.task_repository.get_completion_rate(db, user_id)
        stats['completion_rate'] = round(  # type: ignore
            completion_rate * 100, 2)

        # 3. 追加の統計情報
        stats.update(await self._calculate_additional_stats(db, user_id))

        return stats

    async def get_productivity_insights(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """
        生産性に関するインサイトを取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Dict[str, Any]: 生産性インサイト
        """
        # 1. 今日期限のタスク
        due_today = await self.task_repository.get_due_today(db, user_id)

        # 2. 今週期限のタスク
        due_this_week = await self.task_repository.get_due_this_week(db, user_id)

        # 3. 期限切れタスク
        overdue_tasks = await self.task_repository.get_overdue_tasks(db, user_id)

        # 4. 高優先度の未完了タスク
        high_priority_pending = await self.task_repository.get_by_priority(
            db, user_id, 'high'
        )
        high_priority_pending = [
            t for t in high_priority_pending if not t.completed]

        return {
            'due_today_count': len(due_today),
            'due_this_week_count': len(due_this_week),
            'overdue_count': len(overdue_tasks),
            'high_priority_pending_count': len(high_priority_pending),
            'recommendations': await self._generate_recommendations(
                due_today, due_this_week, overdue_tasks, high_priority_pending
            )
        }

    # ====== プライベートメソッド（ビジネスロジック） ======

    async def _validate_task_data(self, task_data) -> None:
        """タスクデータのバリデーション"""
        # タイトルの検証
        if not hasattr(task_data, 'title') or not task_data.title.strip():
            raise ValueError("タイトルは必須です")

        if len(task_data.title) > 200:
            raise ValueError("タイトルは200文字以下である必要があります")

        # 優先度の検証
        if hasattr(task_data, 'priority'):
            valid_priorities = ['low', 'medium', 'high']
            if task_data.priority not in valid_priorities:
                raise ValueError(f"優先度は {valid_priorities} のいずれかである必要があります")

        # 期限日の検証
        if hasattr(task_data, 'due_date') and task_data.due_date:
            if task_data.due_date < datetime.utcnow():
                raise ValueError("期限日は現在日時より後である必要があります")

    async def _validate_task_update_data(self, task_data, existing_task) -> None:
        """タスク更新データのバリデーション"""
        # 基本的なバリデーション
        if hasattr(task_data, 'title') and task_data.title is not None:
            if not task_data.title.strip():
                raise ValueError("タイトルは必須です")
            if len(task_data.title) > 200:
                raise ValueError("タイトルは200文字以下である必要があります")

        # その他のバリデーション...

    async def _check_task_creation_rules(self, db: Session, user_id: int, task_data) -> None:
        """タスク作成時のビジネスルールチェック"""
        # 例: ユーザーあたりの最大タスク数制限
        task_count = await self.task_repository.count_by_user(db, user_id)
        if task_count >= 1000:  # 最大1000タスク
            raise RuntimeError("タスクの上限数に達しています")

    async def _check_task_update_rules(self, db: Session, existing_task, task_data) -> None:
        """タスク更新時のビジネスルールチェック"""
        # 例: 完了済みタスクの特定項目変更禁止
        if existing_task.completed and hasattr(task_data, 'due_date'):
            if task_data.due_date != existing_task.due_date:
                raise RuntimeError("完了済みタスクの期限日は変更できません")

    async def _check_task_deletion_rules(self, db: Session, task) -> None:
        """タスク削除時のビジネスルールチェック"""
        # 例: 特定条件のタスクの削除禁止
        pass

    async def _check_task_completion_rules(self, db: Session, task) -> None:
        """タスク完了時のビジネスルールチェック"""
        # 例: 期限切れタスクの完了時の警告
        if task.due_date and task.due_date < datetime.utcnow():
            # ログ出力や通知などの処理
            pass

    async def _check_task_incompletion_rules(self, db: Session, task) -> None:
        """タスク未完了時のビジネスルールチェック"""
        # 例: 特定条件での未完了への変更禁止
        pass

    async def _calculate_additional_stats(self, db: Session, user_id: int) -> Dict[str, Any]:
        """追加の統計情報を計算"""
        # 今日完了したタスクの数
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        # 実際の実装では、updated_atとcompletedを組み合わせた条件でクエリ
        # ここではサンプルとして空の辞書を返す
        return {
            'completed_today': 0,
            'average_completion_time': 0,
            'most_common_priority': 'medium'
        }

    async def _generate_recommendations(
        self,
        due_today,
        due_this_week,
        overdue_tasks,
        high_priority_pending
    ) -> List[str]:
        """ユーザーへの推奨事項を生成"""
        recommendations = []

        if overdue_tasks:
            recommendations.append(
                f"{len(overdue_tasks)}件の期限切れタスクがあります。優先的に処理してください。")

        if due_today:
            recommendations.append(f"今日期限のタスクが{len(due_today)}件あります。")

        if high_priority_pending:
            recommendations.append(
                f"高優先度の未完了タスクが{len(high_priority_pending)}件あります。")

        if not recommendations:
            recommendations.append("素晴らしい！すべてのタスクが順調に進んでいます。")

        return recommendations


# ======= TaskServiceの特徴 =======

"""
1. ビジネスロジックの集約
   - タスクに関するビジネスルールを一箇所に集約
   - 複雑なビジネスロジックの実装

2. 複数リポジトリの協調
   - TaskRepositoryとUserRepositoryの組み合わせ
   - 横断的なデータ操作

3. トランザクション管理
   - データの整合性保証
   - 複数操作の原子性保証

4. バリデーション
   - ビジネスルールに基づく検証
   - データの整合性チェック

5. 統計・分析機能
   - 複雑な統計情報の計算
   - ユーザーへのインサイト提供

6. 拡張性
   - 新しいビジネスロジックの追加が容易
   - 既存機能への影響を最小化
"""
