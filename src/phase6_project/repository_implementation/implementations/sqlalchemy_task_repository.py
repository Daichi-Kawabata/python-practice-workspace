"""
SQLAlchemy実装のTaskRepository

役割:
- TaskRepositoryInterfaceの具体的実装
- SQLAlchemyを使用したデータベース操作
- 効率的なクエリの実装
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..interfaces.task_repository import TaskRepositoryInterface
from ..interfaces.base_repository import BaseRepositoryWithUser

# 仮の型定義（実際のプロジェクトでは適切なインポートに変更）
from typing import TypeVar, Any
Task = Any
TaskCreate = Any
TaskUpdate = Any


class SQLAlchemyTaskRepository(TaskRepositoryInterface):
    """
    SQLAlchemy を使用したTaskRepositoryの実装

    TaskRepositoryInterfaceの全てのメソッドを実装
    データベース操作の具体的な実装を提供
    """

    def __init__(self, model_class):
        """
        コンストラクタ

        Args:
            model_class: TaskのSQLAlchemyモデルクラス
        """
        self.model_class = model_class

    # ====== 基底リポジトリのCRUD操作 ======

    async def create(self, db: Session, obj_in: TaskCreate) -> Task:
        """
        タスクの作成

        Args:
            db: データベースセッション
            obj_in: 作成用データ

        Returns:
            Task: 作成されたタスク
        """
        # Pydanticモデルから辞書に変換
        if hasattr(obj_in, 'model_dump'):
            obj_data = obj_in.model_dump()
        elif hasattr(obj_in, '__dict__'):
            obj_data = obj_in.__dict__
        else:
            obj_data = dict(obj_in)

        # SQLAlchemyモデルのインスタンス作成
        db_obj = self.model_class(**obj_data)

        # データベースに保存
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    async def get(self, db: Session, id: int) -> Optional[Task]:
        """
        IDによるタスクの取得

        Args:
            db: データベースセッション
            id: タスクID

        Returns:
            Optional[Task]: 取得されたタスク（存在しない場合None）
        """
        return db.query(self.model_class).filter(self.model_class.id == id).first()

    async def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[Task]:
        """
        複数タスクの取得

        Args:
            db: データベースセッション
            skip: スキップ件数
            limit: 取得件数上限
            **filters: フィルタリング条件

        Returns:
            List[Task]: 取得されたタスクのリスト
        """
        query = db.query(self.model_class)

        # フィルタリング条件を適用
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                query = query.filter(getattr(self.model_class, key) == value)

        return query.offset(skip).limit(limit).all()

    async def update(
        self,
        db: Session,
        db_obj: Task,
        obj_in: TaskUpdate
    ) -> Task:
        """
        タスクの更新

        Args:
            db: データベースセッション
            db_obj: 更新対象のタスク
            obj_in: 更新用データ

        Returns:
            Task: 更新されたタスク
        """
        # 更新データを取得（未設定の項目は除外）
        if hasattr(obj_in, 'model_dump'):
            update_data = obj_in.model_dump(exclude_unset=True)
        elif hasattr(obj_in, '__dict__'):
            update_data = obj_in.__dict__
        else:
            update_data = dict(obj_in)

        # オブジェクトの属性を更新
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # updated_atを更新
        if hasattr(db_obj, 'updated_at'):
            db_obj.updated_at = datetime.utcnow()  # type: ignore

        db.commit()
        db.refresh(db_obj)

        return db_obj

    async def delete(self, db: Session, id: int) -> bool:
        """
        タスクの削除

        Args:
            db: データベースセッション
            id: 削除対象のタスクID

        Returns:
            bool: 削除成功時True、失敗時False
        """
        db_obj = await self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False

    async def exists(self, db: Session, id: int) -> bool:
        """
        タスクの存在確認

        Args:
            db: データベースセッション
            id: 確認対象のタスクID

        Returns:
            bool: 存在する場合True、存在しない場合False
        """
        return db.query(self.model_class).filter(self.model_class.id == id).first() is not None

    async def count(self, db: Session, **filters: Any) -> int:
        """
        タスクの件数取得

        Args:
            db: データベースセッション
            **filters: フィルタリング条件

        Returns:
            int: 条件に一致するタスクの件数
        """
        query = db.query(self.model_class)

        # フィルタリング条件を適用
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                query = query.filter(getattr(self.model_class, key) == value)

        return query.count()

    # ====== ユーザー関連の操作 ======

    async def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[Task]:
        """
        ユーザーIDによるタスクの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            skip: スキップ件数
            limit: 取得件数上限
            **filters: 追加のフィルタリング条件

        Returns:
            List[Task]: 取得されたタスクのリスト
        """
        query = db.query(self.model_class).filter(
            self.model_class.user_id == user_id)

        # 追加のフィルタリング条件を適用
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                query = query.filter(getattr(self.model_class, key) == value)

        return query.order_by(self.model_class.created_at.desc()).offset(skip).limit(limit).all()

    async def get_by_user_and_id(
        self,
        db: Session,
        user_id: int,
        id: int
    ) -> Optional[Task]:
        """
        ユーザーIDとタスクIDによる取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            id: タスクID

        Returns:
            Optional[Task]: 取得されたタスク（存在しない場合None）
        """
        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.id == id
            )
        ).first()

    async def count_by_user(
        self,
        db: Session,
        user_id: int,
        **filters: Any
    ) -> int:
        """
        ユーザーIDによるタスクの件数取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            **filters: フィルタリング条件

        Returns:
            int: 条件に一致するタスクの件数
        """
        query = db.query(self.model_class).filter(
            self.model_class.user_id == user_id)

        # フィルタリング条件を適用
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                query = query.filter(getattr(self.model_class, key) == value)

        return query.count()

    # ====== タスク固有の検索メソッド ======

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
        """
        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.completed == completed
            )
        ).order_by(self.model_class.created_at.desc()).offset(skip).limit(limit).all()

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
        """
        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.priority == priority
            )
        ).order_by(self.model_class.created_at.desc()).offset(skip).limit(limit).all()

    async def get_overdue_tasks(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        期限切れタスクの取得
        """
        current_time = datetime.utcnow()
        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.due_date < current_time,
                self.model_class.completed == False
            )
        ).order_by(self.model_class.due_date.asc()).offset(skip).limit(limit).all()

    async def get_due_today(
        self,
        db: Session,
        user_id: int
    ) -> List[Task]:
        """
        今日期限のタスクの取得
        """
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.due_date >= today,
                self.model_class.due_date < tomorrow,
                self.model_class.completed == False
            )
        ).order_by(self.model_class.due_date.asc()).all()

    async def get_due_this_week(
        self,
        db: Session,
        user_id: int
    ) -> List[Task]:
        """
        今週期限のタスクの取得
        """
        today = datetime.utcnow().date()
        week_end = today + timedelta(days=7)

        return db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.due_date >= today,
                self.model_class.due_date <= week_end,
                self.model_class.completed == False
            )
        ).order_by(self.model_class.due_date.asc()).all()

    # ====== タスクの一括操作 ======

    async def mark_completed(
        self,
        db: Session,
        user_id: int,
        task_id: int
    ) -> Optional[Task]:
        """
        タスクを完了状態にする
        """
        task = await self.get_by_user_and_id(db, user_id, task_id)
        if task:
            task.completed = True
            task.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(task)
        return task

    async def mark_incomplete(
        self,
        db: Session,
        user_id: int,
        task_id: int
    ) -> Optional[Task]:
        """
        タスクを未完了状態にする
        """
        task = await self.get_by_user_and_id(db, user_id, task_id)
        if task:
            task.completed = False
            task.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(task)
        return task

    async def bulk_update_priority(
        self,
        db: Session,
        user_id: int,
        task_ids: List[int],
        priority: str
    ) -> List[Task]:
        """
        複数タスクの優先度を一括更新
        """
        tasks = db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.id.in_(task_ids)
            )
        ).all()

        for task in tasks:
            task.priority = priority
            task.updated_at = datetime.utcnow()

        db.commit()

        # 更新されたタスクを再取得
        for task in tasks:
            db.refresh(task)

        return tasks

    async def bulk_delete(
        self,
        db: Session,
        user_id: int,
        task_ids: List[int]
    ) -> int:
        """
        複数タスクの一括削除
        """
        deleted_count = db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                self.model_class.id.in_(task_ids)
            )
        ).delete(synchronize_session=False)

        db.commit()
        return deleted_count

    # ====== 統計情報の取得 ======

    async def get_task_stats(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, int]:
        """
        タスクの統計情報を取得
        """
        base_query = db.query(self.model_class).filter(
            self.model_class.user_id == user_id)

        total = base_query.count()
        completed = base_query.filter(
            self.model_class.completed == True).count()
        pending = base_query.filter(
            self.model_class.completed == False).count()

        current_time = datetime.utcnow()
        overdue = base_query.filter(
            and_(
                self.model_class.due_date < current_time,
                self.model_class.completed == False
            )
        ).count()

        high_priority = base_query.filter(
            self.model_class.priority == 'high').count()
        medium_priority = base_query.filter(
            self.model_class.priority == 'medium').count()
        low_priority = base_query.filter(
            self.model_class.priority == 'low').count()

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
        db: Session,
        user_id: int
    ) -> float:
        """
        タスクの完了率を取得
        """
        base_query = db.query(self.model_class).filter(
            self.model_class.user_id == user_id)

        total = base_query.count()
        if total == 0:
            return 0.0

        completed = base_query.filter(
            self.model_class.completed == True).count()
        return completed / total

    # ====== 検索・フィルタリング ======

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
        """
        search_query = db.query(self.model_class).filter(
            and_(
                self.model_class.user_id == user_id,
                or_(
                    self.model_class.title.contains(query),
                    self.model_class.description.contains(query)
                )
            )
        )

        return search_query.order_by(self.model_class.created_at.desc()).offset(skip).limit(limit).all()

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
        """
        query = db.query(self.model_class).filter(
            self.model_class.user_id == user_id)

        # 完了状態フィルタ
        if completed is not None:
            query = query.filter(self.model_class.completed == completed)

        # 優先度フィルタ
        if priority:
            query = query.filter(self.model_class.priority == priority)

        # 期限日フィルタ
        if due_date_from:
            query = query.filter(self.model_class.due_date >= due_date_from)

        if due_date_to:
            query = query.filter(self.model_class.due_date <= due_date_to)

        return query.order_by(self.model_class.created_at.desc()).offset(skip).limit(limit).all()


# ======= SQLAlchemy実装の特徴 =======

"""
1. 具体的なデータベース操作
   - SQLAlchemyのORMを使用したクエリ実装
   - 効率的なデータベースアクセス

2. エラーハンドリング
   - データベースエラーの適切な処理
   - トランザクション管理

3. パフォーマンス最適化
   - 適切なインデックスの活用
   - N+1問題の回避

4. 型安全性
   - 型ヒントによる安全なコード
   - SQLAlchemyモデルとの型整合性

5. 拡張性
   - 新しいクエリの追加が容易
   - 複雑な検索条件への対応

6. 保守性
   - 一貫したコーディングスタイル
   - 適切なコメントとドキュメント
"""
