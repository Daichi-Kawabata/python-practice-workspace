"""
SQLAlchemy データベース接続とセッション管理
このモジュールは、SQLAlchemyを使用してデータベース接続とセッション管理を行います。
"""

import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class DatabaseManager:
    """データベース接続とセッション管理を行うクラス"""

    def __init__(self, database_url: str = "sqlite:///./todo_api.db") -> None:
        """
        データベースマネージャーを初期化

        Args:
            database_url: データベース接続URL（デフォルト: SQLite）
        """
        # HerokuのDATABASE_URLを優先し、なければローカルSQLite
        url = database_url or os.environ.get(
            "DATABASE_URL", "sqlite:///./todo_api.db")
        # PostgreSQLのURL修正
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        self.database_url: str = url
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None

    def create_engine_and_session(self) -> None:
        """エンジンとセッションファクトリを作成"""
        self.engine = create_engine(
            self.database_url,
            echo=True,  # SQLログを表示
            connect_args={
                "check_same_thread": False} if "sqlite" in self.database_url else {}
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def create_tables(self) -> None:
        """全てのテーブルを作成"""
        if self.engine is None:
            raise ValueError("Engine が初期化されていません")

        # すべてのモデルからテーブルを作成
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """新しいセッションを取得"""
        if self.SessionLocal is None:
            raise ValueError("SessionLocal が初期化されていません")

        return self.SessionLocal()

    def close_engine(self) -> None:
        """エンジンを閉じる"""
        if self.engine:
            self.engine.dispose()


db_manager = DatabaseManager()


def init_db() -> None:
    """データベースの初期化"""
    db_manager.create_engine_and_session()
    db_manager.create_tables()
    print("データベースが初期化されました。")


def get_db_session() -> Session:
    """データベースセッションを取得（with文で使用推奨）"""
    return db_manager.get_session()


# 使用例とテスト用コード
if __name__ == "__main__":
    print("🔧 データベース接続テスト")

    try:
        # データベース初期化
        init_db()

        # セッション取得テスト
        with get_db_session() as session:
            print("✅ セッション作成成功")
            # ここで実際のデータベース操作を行う

        print("✅ データベース接続テスト完了")

    except Exception as e:
        print(f"❌ エラー: {e}")
    finally:
        db_manager.close_engine()
