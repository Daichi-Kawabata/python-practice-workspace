"""
Model層 - Userモデル
MVCパターンにおけるModel層の実装例

役割:
- ユーザーデータの構造定義
- 認証関連のビジネスロジック
- パスワードハッシュ化の処理
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from passlib.context import CryptContext
from typing import Optional, List

Base = declarative_base()

# パスワードハッシュ化のための設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    Userモデル - MVCのModel層

    責任:
    - ユーザーデータの構造定義
    - パスワードの暗号化・検証
    - 基本的なユーザー情報の管理
    """
    __tablename__ = "users"

    # 主キー
    id = Column(Integer, primary_key=True, index=True)

    # ユーザー情報
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # ユーザーの状態
    is_active = Column(Boolean, default=True, nullable=False)

    # タイムスタンプ
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # リレーションシップ
    tasks = relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    # ======= Model層のビジネスロジック =======

    def set_password(self, password: str) -> None:
        """
        パスワードをハッシュ化して設定

        Args:
            password: 平文のパスワード
        """
        self.hashed_password = pwd_context.hash(password)
        self.updated_at = datetime.utcnow()

    def verify_password(self, password: str) -> bool:
        """
        パスワードを検証

        Args:
            password: 検証する平文のパスワード

        Returns:
            bool: パスワードが正しい場合True
        """
        return pwd_context.verify(password, self.hashed_password)

    def activate(self) -> None:
        """
        ユーザーをアクティブにする
        """
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """
        ユーザーを非アクティブにする
        """
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def get_active_tasks_count(self) -> int:
        """
        アクティブなタスクの数を取得

        Returns:
            int: 未完了タスクの数
        """
        return len([task for task in self.tasks if not task.completed])

    def get_completed_tasks_count(self) -> int:
        """
        完了したタスクの数を取得

        Returns:
            int: 完了タスクの数
        """
        return len([task for task in self.tasks if task.completed])

    def get_overdue_tasks_count(self) -> int:
        """
        期限切れタスクの数を取得

        Returns:
            int: 期限切れタスクの数
        """
        return len([task for task in self.tasks if task.is_overdue()])

    def to_dict(self, include_stats: bool = False) -> dict:
        """
        モデルを辞書形式に変換

        Args:
            include_stats: タスク統計を含めるかどうか

        Returns:
            dict: ユーザーの辞書表現
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        if include_stats:
            user_dict.update({
                "tasks_count": len(self.tasks),
                "active_tasks_count": self.get_active_tasks_count(),
                "completed_tasks_count": self.get_completed_tasks_count(),
                "overdue_tasks_count": self.get_overdue_tasks_count(),
            })

        return user_dict

    @classmethod
    def validate_user_data(cls, username: str, email: str, password: str) -> None:
        """
        ユーザーデータのバリデーション

        Args:
            username: ユーザー名
            email: メールアドレス
            password: パスワード

        Raises:
            ValueError: バリデーションエラー
        """
        # ユーザー名の検証
        if not username or not username.strip():
            raise ValueError("ユーザー名は必須です")

        if len(username) < 3:
            raise ValueError("ユーザー名は3文字以上である必要があります")

        if len(username) > 50:
            raise ValueError("ユーザー名は50文字以下である必要があります")

        # メールアドレスの検証
        if not email or not email.strip():
            raise ValueError("メールアドレスは必須です")

        if "@" not in email:
            raise ValueError("有効なメールアドレスを入力してください")

        # パスワードの検証
        if not password:
            raise ValueError("パスワードは必須です")

        if len(password) < 8:
            raise ValueError("パスワードは8文字以上である必要があります")

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        """
        メールアドレスの形式チェック

        Args:
            email: チェックするメールアドレス

        Returns:
            bool: 有効な形式の場合True
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


# ======= MVCパターンにおけるModel層の特徴 =======

"""
1. データの構造定義
   - ユーザーテーブルのスキーマ定義
   - 適切なデータ型と制約の設定

2. ビジネスロジック
   - パスワードの暗号化・検証
   - ユーザー状態の管理
   - タスク統計の計算

3. データ検証
   - ユーザー登録時のバリデーション
   - メールアドレスの形式チェック

4. セキュリティ
   - パスワードのハッシュ化
   - 平文パスワードの保存を防止

5. 関連データの管理
   - タスクとのリレーションシップ
   - 関連データの統計情報提供
"""
