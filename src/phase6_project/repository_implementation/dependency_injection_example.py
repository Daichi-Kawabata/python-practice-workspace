"""
依存性注入の詳細な仕組み解説

このファイルでは、抽象インターフェースから具体的な実装への
マッピングがどのように行われるかを詳しく説明します。
"""

from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

# ======= 1. 抽象インターフェースの定義 =======


@runtime_checkable
class TaskRepositoryInterface(Protocol):
    """タスクリポジトリのインターフェース"""

    def create(self, task_data: dict) -> dict:
        """タスクを作成"""
        ...

    def get_by_id(self, task_id: int) -> dict:
        """IDでタスクを取得"""
        ...


# ======= 2. 具体的な実装クラス =======

class SQLAlchemyTaskRepository:
    """SQLAlchemy実装"""

    def __init__(self, db_session):
        self.db_session = db_session
        print("SQLAlchemyTaskRepository が初期化されました")

    def create(self, task_data: dict) -> dict:
        print(f"SQLAlchemy: タスクを作成します - {task_data}")
        # 実際のSQLAlchemy処理
        return {"id": 1, "title": task_data["title"], "created_with": "SQLAlchemy"}

    def get_by_id(self, task_id: int) -> dict:
        print(f"SQLAlchemy: タスクID {task_id} を取得します")
        return {"id": task_id, "title": "SQLAlchemy Task", "source": "database"}


class MockTaskRepository:
    """モック実装（テスト用）"""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        print("MockTaskRepository が初期化されました")

    def create(self, task_data: dict) -> dict:
        print(f"Mock: タスクを作成します - {task_data}")
        # メモリ上での処理
        task = {"id": self.next_id,
                "title": task_data["title"], "created_with": "Mock"}
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_by_id(self, task_id: int) -> dict:
        print(f"Mock: タスクID {task_id} を取得します")
        return self.tasks.get(task_id, {"id": task_id, "title": "Mock Task", "source": "memory"})


# ======= 3. サービス層 =======

class TaskService:
    """タスクサービス"""

    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository
        print(f"TaskService が初期化されました。リポジトリ: {type(task_repository).__name__}")

    def create_task(self, task_data: dict) -> dict:
        print("TaskService: タスク作成を開始")
        # ビジネスロジック
        if not task_data.get("title"):
            raise ValueError("タイトルは必須です")

        # リポジトリのメソッドを呼び出し
        # ここで具体的な実装のメソッドが実行される
        result = self.task_repository.create(task_data)
        print(f"TaskService: タスク作成完了 - {result}")
        return result

    def get_task(self, task_id: int) -> dict:
        print(f"TaskService: タスク取得を開始 - ID: {task_id}")
        # リポジトリのメソッドを呼び出し
        result = self.task_repository.get_by_id(task_id)
        print(f"TaskService: タスク取得完了 - {result}")
        return result


# ======= 4. 依存性注入の設定 =======

class AppConfig:
    """アプリケーション設定"""

    def __init__(self):
        self.USE_MOCK_DATA: bool = True  # 切り替え可能


# ファクトリー関数
def create_task_repository(config: AppConfig) -> TaskRepositoryInterface:
    """タスクリポジトリの作成"""
    print(f"リポジトリを作成中... モック使用: {config.USE_MOCK_DATA}")

    if config.USE_MOCK_DATA:
        return MockTaskRepository()
    else:
        # 実際のプロジェクトでは適切なDBセッションを渡す
        return SQLAlchemyTaskRepository(db_session=None)


def create_task_service(config: AppConfig) -> TaskService:
    """タスクサービスの作成"""
    print("TaskServiceを作成中...")

    # 1. リポジトリの具体的な実装を取得
    task_repository = create_task_repository(config)

    # 2. サービスに注入
    return TaskService(task_repository)


# ======= 5. 実行例 =======

def demonstrate_dependency_injection():
    """依存性注入のデモンストレーション"""

    print("=" * 50)
    print("依存性注入のデモンストレーション")
    print("=" * 50)

    # 設定1: モック実装を使用
    print("\n【パターン1: モック実装を使用】")
    config_mock = AppConfig()
    config_mock.USE_MOCK_DATA = True

    service_mock = create_task_service(config_mock)

    # タスクの作成
    task_data = {"title": "テストタスク", "description": "これはテストです"}
    created_task = service_mock.create_task(task_data)

    # タスクの取得
    retrieved_task = service_mock.get_task(created_task["id"])

    print("\n" + "-" * 30)

    # 設定2: SQLAlchemy実装を使用
    print("\n【パターン2: SQLAlchemy実装を使用】")
    config_db = AppConfig()
    config_db.USE_MOCK_DATA = False

    service_db = create_task_service(config_db)

    # 同じインターフェースだが、異なる実装が実行される
    created_task_db = service_db.create_task(task_data)
    retrieved_task_db = service_db.get_task(1)

    print("\n" + "=" * 50)
    print("重要なポイント:")
    print("1. TaskServiceのコードは一切変更していない")
    print("2. 設定を変更するだけで異なる実装が使用される")
    print("3. サービス層は具体的な実装を知らない")
    print("=" * 50)


# ======= 6. FastAPIでの実際の使用例 =======

class FastAPIExample:
    """FastAPIでの依存性注入例"""

    def __init__(self):
        self.config = AppConfig()

    def get_task_repository(self) -> TaskRepositoryInterface:
        """FastAPIの依存性注入で使用される関数"""
        return create_task_repository(self.config)

    def get_task_service(self) -> TaskService:
        """FastAPIの依存性注入で使用される関数"""
        return create_task_service(self.config)

    async def create_task_endpoint(
        self,
        task_data: dict,
        task_service: TaskService  # ← ここで注入される
    ) -> dict:
        """
        FastAPIエンドポイント

        実際の使用では:
        task_service: TaskService = Depends(get_task_service)
        """
        return task_service.create_task(task_data)


# ======= 実行 =======

if __name__ == "__main__":
    demonstrate_dependency_injection()


# ======= まとめ =======

"""
依存性注入の仕組み:

1. **抽象化**: インターフェースで操作を定義
2. **具体化**: 複数の実装クラスを作成
3. **ファクトリー**: 設定に基づいて適切な実装を選択
4. **注入**: サービス層に具体的な実装を注入
5. **実行**: サービス層は抽象インターフェースを通じて操作

利点:
- テスタビリティ: モック実装で簡単にテスト可能
- 柔軟性: 実装を簡単に切り替え可能
- 保守性: 新しい実装を追加しても既存コードに影響なし
- 分離: 各層が疎結合で独立している
"""
