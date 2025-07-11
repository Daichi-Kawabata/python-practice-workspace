"""
Repositoryパターンの基底インターフェース

役割:
- 共通的なCRUD操作の定義
- 各具体的リポジトリの基底となるインターフェース
- 一貫した操作方法の提供
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any
from sqlalchemy.orm import Session

# 型変数の定義
T = TypeVar('T')  # エンティティの型
CreateSchema = TypeVar('CreateSchema')  # 作成用スキーマの型
UpdateSchema = TypeVar('UpdateSchema')  # 更新用スキーマの型


class BaseRepository(ABC, Generic[T, CreateSchema, UpdateSchema]):
    """
    基底リポジトリインターフェース

    Repositoryパターンの基本的なCRUD操作を定義
    各具体的リポジトリはこのインターフェースを実装する
    """

    @abstractmethod
    async def create(self, db: Session, obj_in: CreateSchema) -> T:
        """
        エンティティの作成

        Args:
            db: データベースセッション
            obj_in: 作成用データ

        Returns:
            T: 作成されたエンティティ
        """
        pass

    @abstractmethod
    async def get(self, db: Session, id: int) -> Optional[T]:
        """
        IDによるエンティティの取得

        Args:
            db: データベースセッション
            id: エンティティのID

        Returns:
            Optional[T]: 取得されたエンティティ（存在しない場合None）
        """
        pass

    @abstractmethod
    async def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[T]:
        """
        複数エンティティの取得

        Args:
            db: データベースセッション
            skip: スキップ件数
            limit: 取得件数上限
            **filters: フィルタリング条件

        Returns:
            List[T]: 取得されたエンティティのリスト
        """
        pass

    @abstractmethod
    async def update(
        self,
        db: Session,
        db_obj: T,
        obj_in: UpdateSchema
    ) -> T:
        """
        エンティティの更新

        Args:
            db: データベースセッション
            db_obj: 更新対象のエンティティ
            obj_in: 更新用データ

        Returns:
            T: 更新されたエンティティ
        """
        pass

    @abstractmethod
    async def delete(self, db: Session, id: int) -> bool:
        """
        エンティティの削除

        Args:
            db: データベースセッション
            id: 削除対象のエンティティID

        Returns:
            bool: 削除成功時True、失敗時False
        """
        pass

    @abstractmethod
    async def exists(self, db: Session, id: int) -> bool:
        """
        エンティティの存在確認

        Args:
            db: データベースセッション
            id: 確認対象のエンティティID

        Returns:
            bool: 存在する場合True、存在しない場合False
        """
        pass

    @abstractmethod
    async def count(self, db: Session, **filters: Any) -> int:
        """
        エンティティの件数取得

        Args:
            db: データベースセッション
            **filters: フィルタリング条件

        Returns:
            int: 条件に一致するエンティティの件数
        """
        pass


class BaseRepositoryWithUser(BaseRepository[T, CreateSchema, UpdateSchema]):
    """
    ユーザーに関連するエンティティのための基底リポジトリ

    ユーザーIDによるフィルタリング機能を追加
    """

    @abstractmethod
    async def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        **filters: Any
    ) -> List[T]:
        """
        ユーザーIDによるエンティティの取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            skip: スキップ件数
            limit: 取得件数上限
            **filters: 追加のフィルタリング条件

        Returns:
            List[T]: 取得されたエンティティのリスト
        """
        pass

    @abstractmethod
    async def get_by_user_and_id(
        self,
        db: Session,
        user_id: int,
        id: int
    ) -> Optional[T]:
        """
        ユーザーIDとエンティティIDによる取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            id: エンティティID

        Returns:
            Optional[T]: 取得されたエンティティ（存在しない場合None）
        """
        pass

    @abstractmethod
    async def count_by_user(
        self,
        db: Session,
        user_id: int,
        **filters: Any
    ) -> int:
        """
        ユーザーIDによるエンティティの件数取得

        Args:
            db: データベースセッション
            user_id: ユーザーID
            **filters: フィルタリング条件

        Returns:
            int: 条件に一致するエンティティの件数
        """
        pass


# ======= Repositoryパターンの基底インターフェースの特徴 =======

"""
1. 抽象化
   - 具体的な実装の詳細を隠蔽
   - 統一されたインターフェースを提供

2. 型安全性
   - ジェネリクスを使用した型安全な実装
   - コンパイル時の型チェック

3. 一貫性
   - 全てのリポジトリで共通の操作方法
   - 統一されたメソッド名と引数

4. 拡張性
   - 基底クラスを継承して機能追加
   - 特定のドメインに特化した操作の追加

5. テスタビリティ
   - インターフェースに基づいたモック作成
   - 依存性の逆転による単体テストの容易さ

6. 保守性
   - 変更の影響範囲を限定
   - 実装の詳細変更時の影響を最小化
"""
