# Web アプリケーション設計パターンガイド

## 1. MVC パターン（Model-View-Controller）

### 概要

MVC パターンは、アプリケーションを 3 つの主要なコンポーネントに分離する設計パターンです。

### 各コンポーネントの役割

#### Model（モデル）

- **役割**: データとビジネスロジックの管理
- **責任**:
  - データベースとの相互作用
  - データの検証
  - ビジネスルールの実装
- **FastAPI での実装**: SQLAlchemy モデル、Pydantic スキーマ

#### View（ビュー）

- **役割**: ユーザーインターフェースの表示
- **責任**:
  - データの表示形式の決定
  - ユーザーへの情報提示
- **FastAPI での実装**: JSON レスポンス、HTML テンプレート

#### Controller（コントローラー）

- **役割**: ユーザーの入力を処理し、Model と View を調整
- **責任**:
  - HTTP リクエストの処理
  - 適切な Model メソッドの呼び出し
  - レスポンスの構築
- **FastAPI での実装**: API エンドポイント（ルーター）

### MVC パターンの利点

1. **関心の分離**: 各層が独立した責任を持つ
2. **保守性**: 変更の影響範囲が限定的
3. **テスタビリティ**: 各層を独立してテスト可能
4. **再利用性**: コンポーネントの再利用が容易

## 2. Repository パターン

### 概要

Repository パターンは、データアクセスロジックを抽象化し、ビジネスロジックからデータストレージの詳細を隠蔽する設計パターンです。

### 構成要素

#### Repository Interface（リポジトリインターフェース）

- データアクセスメソッドの抽象定義
- 実装の詳細を隠蔽

#### Concrete Repository（具体的リポジトリ）

- インターフェースの具体的実装
- 実際のデータベース操作

#### Entity（エンティティ）

- ドメインオブジェクト
- ビジネスルールを含む

### Repository パターンの利点

1. **テスタビリティ**: モックによるテストが容易
2. **保守性**: データアクセスロジックが集約
3. **柔軟性**: 異なるデータストレージへの切り替えが容易
4. **再利用性**: 複数のサービスで共通利用

## 3. 設計パターンの組み合わせ

### MVC + Repository の構成

```
┌─────────────────┐
│   Controller    │ ← HTTP リクエスト
│   (Router)      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    Service      │ ← ビジネスロジック
│                 │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Repository    │ ← データアクセス
│   (Interface)   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Concrete Repo   │ ← 具体的実装
│ (SQLAlchemy)    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    Database     │
└─────────────────┘
```

### レイヤー間の依存関係

1. **Controller** → **Service** → **Repository Interface**
2. **Repository Implementation** → **Database**
3. **依存性注入**により、上位層は下位層の実装詳細を知らない

## 4. 実装のベストプラクティス

### 1. 単一責任の原則

- 各クラスは一つの責任のみを持つ
- 変更の理由は一つに限定

### 2. 依存性の逆転

- 上位層は下位層の抽象に依存
- 具体的な実装ではなくインターフェースに依存

### 3. インターフェース分離

- 不必要な依存関係を避ける
- 必要な機能のみを公開

### 4. 開放閉鎖の原則

- 拡張に対して開放
- 変更に対して閉鎖

## 5. FastAPI での実装例

### ディレクトリ構造

```
app/
├── controllers/     # コントローラー層
│   ├── __init__.py
│   └── task_controller.py
├── services/        # サービス層（ビジネスロジック）
│   ├── __init__.py
│   └── task_service.py
├── repositories/    # リポジトリ層
│   ├── __init__.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── task_repository.py
│   └── implementations/
│       ├── __init__.py
│       └── sqlalchemy_task_repository.py
├── models/         # データモデル
│   ├── __init__.py
│   └── task.py
└── schemas/        # APIスキーマ
    ├── __init__.py
    └── task.py
```

### コード例（概要）

#### Repository Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: TaskCreate) -> Task:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all(self, user_id: int) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        pass
```

#### Service Layer

```python
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: TaskCreate, user_id: int) -> Task:
        # ビジネスロジック（例：バリデーション）
        if not task.title.strip():
            raise ValueError("タイトルは必須です")

        # リポジトリを使用してデータ操作
        return await self.repository.create(task)
```

#### Controller Layer

```python
@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create_task(task, current_user.id)
```

## 6. 学習のポイント

1. **段階的な理解**: まず MVC から始めて、徐々に Repository パターンを追加
2. **理論と実装の対応**: 各パターンの概念と具体的な実装方法の理解
3. **設計の利点**: 設計パターンがもたらす保守性・テスタビリティの向上
4. **トレードオフの理解**: 複雑性の増加と保守性の向上のバランス

## 7. まとめ

設計パターンは、コードの品質を向上させるための強力なツールです：

1. **MVC パターン**: 関心の分離により、各層の責任を明確化
2. **Repository パターン**: データアクセスの抽象化により、テスタビリティとメンテナンス性を向上
3. **組み合わせ**: 複数のパターンを組み合わせることで、より堅牢なアーキテクチャを構築

これらの知識を活用して、保守性の高い Web アプリケーションを開発してください。
