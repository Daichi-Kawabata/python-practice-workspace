"""
UserRepositoryインターフェース

役割:
- ユーザーに関するデータアクセス操作の定義
- ユーザー固有の操作方法の抽象化
- 実装の詳細の隠蔽
"""

from abc import abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session

from .base_repository import BaseRepository

# 仮の型定義（実際のプロジェクトでは適切なインポートに変更）
from typing import TypeVar
User = TypeVar('User')
UserCreate = TypeVar('UserCreate')
UserUpdate = TypeVar('UserUpdate')


class UserRepositoryInterface(BaseRepository[User, UserCreate, UserUpdate]):
    """
    ユーザーリポジトリインターフェース

    ユーザーに関するデータアクセス操作を定義
    BaseRepositoryの基本CRUD操作に加えて、
    ユーザー固有の操作を追加
    """

    @abstractmethod
    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        メールアドレスでユーザーを取得

        Args:
            db: データベースセッション
            email: メールアドレス

        Returns:
            Optional[User]: ユーザー（存在しない場合None）
        """
        pass

    @abstractmethod
    async def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        ユーザー名でユーザーを取得

        Args:
            db: データベースセッション
            username: ユーザー名

        Returns:
            Optional[User]: ユーザー（存在しない場合None）
        """
        pass

    @abstractmethod
    async def is_email_taken(self, db: Session, email: str) -> bool:
        """
        メールアドレスが既に使用されているかチェック

        Args:
            db: データベースセッション
            email: メールアドレス

        Returns:
            bool: 使用されている場合True
        """
        pass

    @abstractmethod
    async def is_username_taken(self, db: Session, username: str) -> bool:
        """
        ユーザー名が既に使用されているかチェック

        Args:
            db: データベースセッション
            username: ユーザー名

        Returns:
            bool: 使用されている場合True
        """
        pass

    @abstractmethod
    async def activate_user(self, db: Session, user_id: int) -> Optional[User]:
        """
        ユーザーをアクティベート

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Optional[User]: アクティベートされたユーザー
        """
        pass

    @abstractmethod
    async def deactivate_user(self, db: Session, user_id: int) -> Optional[User]:
        """
        ユーザーを非アクティベート

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Optional[User]: 非アクティベートされたユーザー
        """
        pass

    @abstractmethod
    async def get_active_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        アクティブなユーザーのリストを取得

        Args:
            db: データベースセッション
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[User]: アクティブなユーザーのリスト
        """
        pass

    @abstractmethod
    async def search_users(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        ユーザーの検索

        Args:
            db: データベースセッション
            query: 検索クエリ
            skip: スキップ件数
            limit: 取得件数上限

        Returns:
            List[User]: 検索結果のユーザーリスト
        """
        pass

    @abstractmethod
    async def update_last_login(self, db: Session, user_id: int) -> Optional[User]:
        """
        最終ログイン時刻を更新

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            Optional[User]: 更新されたユーザー
        """
        pass

    @abstractmethod
    async def get_user_stats(self, db: Session, user_id: int) -> dict:
        """
        ユーザーの統計情報を取得

        Args:
            db: データベースセッション
            user_id: ユーザーID

        Returns:
            dict: 統計情報
        """
        pass
