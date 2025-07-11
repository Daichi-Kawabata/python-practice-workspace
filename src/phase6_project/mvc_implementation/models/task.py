"""
Model層 - Taskモデル
MVCパターンにおけるModel層の実装例

役割:
- データベーステーブルの定義
- データの検証ルール
- 基本的なデータ操作メソッド
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Task(Base):
    """
    Taskモデル - MVCのModel層

    責任:
    - タスクデータの構造定義
    - データベーステーブルのマッピング
    - 基本的なデータ検証
    """
    __tablename__ = "tasks"

    # 主キー
    id = Column(Integer, primary_key=True, index=True)

    # タスクの基本情報
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    # 優先度（low, medium, high）
    priority = Column(String(20), default="medium", nullable=False)

    # 期限
    due_date = Column(DateTime, nullable=True)

    # 外部キー
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # タイムスタンプ
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # リレーションシップ
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

    # ======= Model層のビジネスロジック =======

    def is_overdue(self) -> bool:
        """
        タスクが期限を過ぎているかチェック

        Returns:
            bool: 期限を過ぎている場合True
        """
        if self.due_date is None:
            return False
        return datetime.utcnow() > self.due_date and not bool(self.completed)  # type: ignore

    def mark_completed(self) -> None:
        """
        タスクを完了状態にする
        """
        self.completed = True
        self.updated_at = datetime.utcnow()

    def mark_incomplete(self) -> None:
        """
        タスクを未完了状態にする
        """
        self.completed = False
        self.updated_at = datetime.utcnow()

    def update_priority(self, new_priority: str) -> None:
        """
        優先度を更新する

        Args:
            new_priority: 新しい優先度（low, medium, high）

        Raises:
            ValueError: 無効な優先度が指定された場合
        """
        valid_priorities = ["low", "medium", "high"]
        if new_priority not in valid_priorities:
            raise ValueError(f"優先度は {valid_priorities} のいずれかである必要があります")

        self.priority = new_priority
        self.updated_at = datetime.utcnow()

    def set_due_date(self, due_date: Optional[datetime]) -> None:
        """
        期限日を設定する

        Args:
            due_date: 期限日（Noneの場合は期限なし）

        Raises:
            ValueError: 過去の日付が指定された場合
        """
        if due_date and due_date < datetime.utcnow():
            raise ValueError("期限日は現在日時より後である必要があります")

        self.due_date = due_date
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """
        モデルを辞書形式に変換

        Returns:
            dict: タスクの辞書表現
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date is not None else None,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_overdue": self.is_overdue()
        }

    @classmethod
    def validate_task_data(cls, title: str, priority: str = "medium") -> None:
        """
        タスクデータのバリデーション

        Args:
            title: タスクのタイトル
            priority: 優先度

        Raises:
            ValueError: バリデーションエラー
        """
        if not title or not title.strip():
            raise ValueError("タイトルは必須です")

        if len(title) > 200:
            raise ValueError("タイトルは200文字以下である必要があります")

        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            raise ValueError(f"優先度は {valid_priorities} のいずれかである必要があります")


# ======= MVCパターンにおけるModel層の特徴 =======

"""
1. データの構造定義
   - SQLAlchemyのORM機能を使用してデータベーステーブルを定義
   - カラムの型、制約、リレーションシップを明確に定義

2. ビジネスロジック
   - データに関連するビジネスルールを実装
   - 例: is_overdue(), mark_completed(), update_priority()

3. データ検証
   - データの整合性を保つための検証ロジック
   - 例: validate_task_data()

4. 責任の範囲
   - データの構造と基本的な操作のみを担当
   - データベースへの永続化は別の層（Repository）が担当
   - HTTP処理やレスポンス形式は別の層が担当

5. 再利用性
   - 他の層やコンポーネントから利用可能
   - ビジネスロジックが集約されているため、一貫性を保てる
"""
