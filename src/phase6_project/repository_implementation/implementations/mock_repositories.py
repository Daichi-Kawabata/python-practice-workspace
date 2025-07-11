"""
テスト用のモックRepository実装

役割:
- テスト用のインメモリ実装
- 実際のデータベースを使用しないテスト
- 高速なテスト実行
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..interfaces.task_repository import TaskRepositoryInterface

# テスト用のデータクラス


class MockTask:
    """テスト用のタスクモデル"""

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.completed = kwargs.get('completed', False)
        self.priority = kwargs.get('priority', 'medium')
        self.due_date = kwargs.get('due_date')
        self.user_id = kwargs.get('user_id')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class MockTaskRepository(TaskRepositoryInterface):
    """
    テスト用のTaskRepositoryモック実装

    インメモリでタスクデータを管理
    テスト時にデータベースを使用せずに動作確認が可能
    """

    def __init__(self):
        """コンストラクタ"""
        self._tasks: Dict[int, MockTask] = {}
        self._next_id = 1

    def clear(self):
        """テスト用：データをクリア"""
        self._tasks.clear()
        self._next_id = 1

    def add_test_data(self, tasks: List[Dict]):
        """テスト用：テストデータを追加"""
        for task_data in tasks:
            task = MockTask(**task_data)
            if not task.id:
                task.id = self._next_id
                self._next_id += 1
            self._tasks[task.id] = task

    # ====== 基底リポジトリのCRUD操作 ======

    async def create(self, db, obj_in) -> MockTask:
        """タスクの作成"""
        task_data = obj_in if isinstance(obj_in, dict) else obj_in.__dict__
        task = MockTask(**task_data)
        task.id = self._next_id
        self._next_id += 1
        self._tasks[task.id] = task
        return task

    async def get(self, db, id: int) -> Optional[MockTask]:
        """IDによるタスクの取得"""
        return self._tasks.get(id)

    async def get_multi(
        self,
        db,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[MockTask]:
        """複数タスクの取得"""
        tasks = list(self._tasks.values())

        # フィルタリング
        for key, value in filters.items():
            tasks = [t for t in tasks if getattr(t, key, None) == value]

        # ページネーション
        return tasks[skip:skip+limit]

    async def update(self, db, db_obj: MockTask, obj_in) -> MockTask:
        """タスクの更新"""
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.__dict__

        for key, value in update_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        db_obj.updated_at = datetime.utcnow()
        return db_obj

    async def delete(self, db, id: int) -> bool:
        """タスクの削除"""
        if id in self._tasks:
            del self._tasks[id]
            return True
        return False

    async def exists(self, db, id: int) -> bool:
        """タスクの存在確認"""
        return id in self._tasks

    async def count(self, db, **filters: Any) -> int:
        """タスクの件数取得"""
        tasks = list(self._tasks.values())

        # フィルタリング
        for key, value in filters.items():
            tasks = [t for t in tasks if getattr(t, key, None) == value]

        return len(tasks)

    # ====== ユーザー関連の操作 ======

    async def get_by_user(
        self,
        db,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[MockTask]:
        """ユーザーIDによるタスクの取得"""
        tasks = [t for t in self._tasks.values() if t.user_id == user_id]

        # フィルタリング
        for key, value in filters.items():
            tasks = [t for t in tasks if getattr(t, key, None) == value]

        # ソート（作成日時の降順）
        tasks.sort(key=lambda t: t.created_at, reverse=True)

        # ページネーション
        return tasks[skip:skip+limit]

    async def get_by_user_and_id(
        self,
        db,
        user_id: int,
        id: int
    ) -> Optional[MockTask]:
        """ユーザーIDとタスクIDによる取得"""
        task = self._tasks.get(id)
        if task and task.user_id == user_id:
            return task
        return None

    async def count_by_user(
        self,
        db,
        user_id: int,
        **filters: Any
    ) -> int:
        """ユーザーIDによるタスクの件数取得"""
        tasks = [t for t in self._tasks.values() if t.user_id == user_id]

        # フィルタリング
        for key, value in filters.items():
            tasks = [t for t in tasks if getattr(t, key, None) == value]

        return len(tasks)

    # ====== タスク固有の検索メソッド ======

    async def get_by_status(
        self,
        db,
        user_id: int,
        completed: bool,
        skip: int = 0,
        limit: int = 100
    ) -> List[MockTask]:
        """完了状態によるタスクの取得"""
        tasks = [t for t in self._tasks.values()
                 if t.user_id == user_id and t.completed == completed]

        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks[skip:skip+limit]

    async def get_by_priority(
        self,
        db,
        user_id: int,
        priority: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MockTask]:
        """優先度によるタスクの取得"""
        tasks = [t for t in self._tasks.values()
                 if t.user_id == user_id and t.priority == priority]

        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks[skip:skip+limit]

    async def get_overdue_tasks(
        self,
        db,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MockTask]:
        """期限切れタスクの取得"""
        current_time = datetime.utcnow()
        tasks = [t for t in self._tasks.values()
                 if (t.user_id == user_id and
                     t.due_date and
                     t.due_date < current_time and
                     not t.completed)]

        tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)
        return tasks[skip:skip+limit]

    async def get_due_today(
        self,
        db,
        user_id: int
    ) -> List[MockTask]:
        """今日期限のタスクの取得"""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        tasks = [t for t in self._tasks.values()
                 if (t.user_id == user_id and
                     t.due_date and
                     today <= t.due_date.date() < tomorrow and
                     not t.completed)]

        tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)
        return tasks

    async def get_due_this_week(
        self,
        db,
        user_id: int
    ) -> List[MockTask]:
        """今週期限のタスクの取得"""
        today = datetime.utcnow().date()
        week_end = today + timedelta(days=7)

        tasks = [t for t in self._tasks.values()
                 if (t.user_id == user_id and
                     t.due_date and
                     today <= t.due_date.date() <= week_end and
                     not t.completed)]

        tasks.sort(key=lambda t: t.due_date if t.due_date else datetime.max)
        return tasks

    # ====== タスクの一括操作 ======

    async def mark_completed(
        self,
        db,
        user_id: int,
        task_id: int
    ) -> Optional[MockTask]:
        """タスクを完了状態にする"""
        task = await self.get_by_user_and_id(db, user_id, task_id)
        if task:
            task.completed = True
            task.updated_at = datetime.utcnow()
        return task

    async def mark_incomplete(
        self,
        db,
        user_id: int,
        task_id: int
    ) -> Optional[MockTask]:
        """タスクを未完了状態にする"""
        task = await self.get_by_user_and_id(db, user_id, task_id)
        if task:
            task.completed = False
            task.updated_at = datetime.utcnow()
        return task

    async def bulk_update_priority(
        self,
        db,
        user_id: int,
        task_ids: List[int],
        priority: str
    ) -> List[MockTask]:
        """複数タスクの優先度を一括更新"""
        updated_tasks = []

        for task_id in task_ids:
            task = await self.get_by_user_and_id(db, user_id, task_id)
            if task:
                task.priority = priority
                task.updated_at = datetime.utcnow()
                updated_tasks.append(task)

        return updated_tasks

    async def bulk_delete(
        self,
        db,
        user_id: int,
        task_ids: List[int]
    ) -> int:
        """複数タスクの一括削除"""
        deleted_count = 0

        for task_id in task_ids:
            task = await self.get_by_user_and_id(db, user_id, task_id)
            if task:
                del self._tasks[task_id]
                deleted_count += 1

        return deleted_count

    # ====== 統計情報の取得 ======

    async def get_task_stats(
        self,
        db,
        user_id: int
    ) -> Dict[str, int]:
        """タスクの統計情報を取得"""
        user_tasks = [t for t in self._tasks.values() if t.user_id == user_id]

        total = len(user_tasks)
        completed = len([t for t in user_tasks if t.completed])
        pending = len([t for t in user_tasks if not t.completed])

        current_time = datetime.utcnow()
        overdue = len([t for t in user_tasks
                      if t.due_date and t.due_date < current_time and not t.completed])

        high_priority = len([t for t in user_tasks if t.priority == 'high'])
        medium_priority = len(
            [t for t in user_tasks if t.priority == 'medium'])
        low_priority = len([t for t in user_tasks if t.priority == 'low'])

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority
        }

    async def get_completion_rate(
        self,
        db,
        user_id: int
    ) -> float:
        """タスクの完了率を取得"""
        user_tasks = [t for t in self._tasks.values() if t.user_id == user_id]

        if not user_tasks:
            return 0.0

        completed = len([t for t in user_tasks if t.completed])
        return completed / len(user_tasks)

    # ====== 検索・フィルタリング ======

    async def search_tasks(
        self,
        db,
        user_id: int,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MockTask]:
        """タスクの検索（タイトル・説明で検索）"""
        query_lower = query.lower()
        tasks = [t for t in self._tasks.values()
                 if (t.user_id == user_id and
                     (query_lower in t.title.lower() or
                      (t.description and query_lower in t.description.lower())))]

        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks[skip:skip+limit]

    async def get_tasks_with_filters(
        self,
        db,
        user_id: int,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MockTask]:
        """複数条件によるタスクの取得"""
        tasks = [t for t in self._tasks.values() if t.user_id == user_id]

        # 完了状態フィルタ
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        # 優先度フィルタ
        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        # 期限日フィルタ
        if due_date_from:
            tasks = [t for t in tasks if t.due_date and t.due_date >= due_date_from]

        if due_date_to:
            tasks = [t for t in tasks if t.due_date and t.due_date <= due_date_to]

        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks[skip:skip+limit]


# ======= モックリポジトリの特徴 =======

"""
1. テスト用実装
   - インメモリでのデータ管理
   - 高速なテスト実行
   - データベースに依存しない

2. テスト支援機能
   - データのクリア機能
   - テストデータの追加機能
   - 状態の確認機能

3. 完全なインターフェース実装
   - 本番実装と同じメソッド
   - 同じ動作を保証

4. デバッグ支援
   - 内部状態の可視化
   - テストデータの操作

5. 開発効率の向上
   - 素早いテスト実行
   - 依存関係の削減
"""
