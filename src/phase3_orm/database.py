"""
SQLAlchemy データベース接続とセッション管理

このファイルでは以下の概念を学習します：
- Engine（データベースエンジン）の作成
- Session（セッション）の管理
- Base（モデルのベースクラス）の定義
- データベースの初期化
"""

from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# SQLAlchemyのBase クラス（全てのモデルの親クラス）
Base = declarative_base()

class DatabaseManager:
    """データベース接続とセッション管理を行うクラス"""
    
    def __init__(self, database_url: str = "sqlite:///./blog.db") -> None:
        """
        データベースマネージャーを初期化
        
        Args:
            database_url: データベース接続URL（デフォルト: SQLite）
        """
        self.database_url = database_url
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None
        
    def create_engine_and_session(self) -> None:
        """エンジンとセッションファクトリを作成"""
        # SQLAlchemyエンジンを作成
        # echo=True で実行されるSQLクエリをコンソールに出力
        self.engine = create_engine(
            self.database_url,
            echo=True,  # SQLログを表示（学習時に便利）
            connect_args={"check_same_thread": False} if "sqlite" in self.database_url else {}
        )
        
        # セッションファクトリを作成
        self.SessionLocal = sessionmaker(
            autocommit=False,  # 手動コミット：トランザクションを手動管理する
            autoflush=False,   # 手動フラッシュ：
            bind=self.engine
        )
        
    def create_tables(self) -> None:
        """全てのテーブルを作成"""
        if self.engine is None:
            raise ValueError("Engine が初期化されていません")
            
        # Base.metadata.create_all() ですべてのモデルからテーブルを作成
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

# グローバルなデータベースマネージャーインスタンス
db_manager = DatabaseManager()

def init_database() -> None:
    """データベースを初期化"""
    db_manager.create_engine_and_session()
    db_manager.create_tables()
    print("✅ データベースが初期化されました")

def get_db_session() -> Session:
    """データベースセッションを取得（with文で使用推奨）"""
    return db_manager.get_session()

# 使用例とテスト用コード
if __name__ == "__main__":
    print("🔧 データベース接続テスト")
    
    try:
        # データベース初期化
        init_database()
        
        # セッション取得テスト
        with get_db_session() as session:
            print("✅ セッション作成成功")
            # ここで実際のデータベース操作を行う
            
        print("✅ データベース接続テスト完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
    finally:
        db_manager.close_engine()
