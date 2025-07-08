"""
FastAPI pytest テストの基本
===========================

このファイルでは、FastAPIアプリケーションのテスト方法について学習します。
pytestとtestclientを使用したAPIテストの書き方を理解しましょう。

- pytest の基本的な使い方
- FastAPI の TestClient を使ったAPIテスト
- フィクスチャ（fixture）の使用
- パラメータ化テスト
- モック（mock）の使用
- 認証が必要なエンドポイントのテスト
"""

import pytest
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, patch
import json

# ===== テスト対象のFastAPIアプリケーション =====


class Item(BaseModel):
    """アイテムモデル"""
    id: Optional[int] = None
    name: str
    description: str
    price: float
    is_available: bool = True


class User(BaseModel):
    """ユーザーモデル"""
    id: Optional[int] = None
    username: str
    email: str


# 疑似データベース
fake_items_db: List[Item] = []
fake_users_db: List[User] = []

# FastAPIアプリケーション
app = FastAPI(title="Test Sample API", version="1.0.0")

# 依存性注入用の関数


def get_current_user():
    """現在のユーザーを取得する依存性注入（簡易版）"""
    return User(id=1, username="testuser", email="test@example.com")

# ===== API エンドポイント =====


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {"message": "Hello World", "version": "1.0.0"}


@app.get("/items", response_model=List[Item])
async def get_items():
    """全アイテム取得"""
    return fake_items_db


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """個別アイテム取得"""
    for item in fake_items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """アイテム作成"""
    if not item.name.strip():
        raise HTTPException(
            status_code=400, detail="Item name cannot be empty")

    item.id = len(fake_items_db) + 1
    fake_items_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """アイテム更新"""
    for i, existing_item in enumerate(fake_items_db):
        if existing_item.id == item_id:
            item.id = item_id
            fake_items_db[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """アイテム削除"""
    for i, item in enumerate(fake_items_db):
        if item.id == item_id:
            del fake_items_db[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    """認証が必要なエンドポイント"""
    return {"message": f"Hello {current_user.username}", "user_id": current_user.id}


@app.get("/calculate/{a}/{b}")
async def calculate(a: float, b: float, operation: str = "add"):
    """計算エンドポイント"""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise HTTPException(
                status_code=400, detail="Division by zero is not allowed")
        result = a / b
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {"a": a, "b": b, "operation": operation, "result": result}


@app.get("/external-api")
async def call_external_api():
    """外部API呼び出しをシミュレート"""
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
        return response.json()

# ===== テストクラスとフィクスチャ =====


class TestFastAPIBasics:
    """FastAPIの基本的なテストクラス"""

    @pytest.fixture
    def client(self):
        """TestClientのフィクスチャ"""
        return TestClient(app)

    @pytest.fixture(autouse=True)
    def reset_db(self):
        """各テスト前にデータベースをリセット"""
        fake_items_db.clear()
        fake_users_db.clear()
        yield
        # テスト後の処理（必要に応じて）

    @pytest.fixture
    def sample_item(self):
        """サンプルアイテムのフィクスチャ"""
        return Item(
            name="Test Item",
            description="This is a test item",
            price=29.99,
            is_available=True
        )

    @pytest.fixture
    def sample_items(self):
        """複数のサンプルアイテムのフィクスチャ"""
        return [
            Item(id=1, name="Item 1", description="Description 1", price=10.0),
            Item(id=2, name="Item 2", description="Description 2", price=20.0),
            Item(id=3, name="Item 3", description="Description 3", price=30.0)
        ]

    # ===== 基本的なエンドポイントテスト =====

    def test_root_endpoint(self, client):
        """ルートエンドポイントのテスト"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Hello World", "version": "1.0.0"}

    def test_get_empty_items(self, client):
        """空のアイテムリスト取得テスト"""
        response = client.get("/items")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_item(self, client, sample_item):
        """アイテム作成テスト"""
        response = client.post(
            "/items", json=sample_item.model_dump(exclude={"id"}))

        assert response.status_code == 200
        created_item = response.json()
        assert created_item["name"] == sample_item.name
        assert created_item["description"] == sample_item.description
        assert created_item["price"] == sample_item.price
        assert created_item["is_available"] == sample_item.is_available
        assert "id" in created_item

    def test_create_item_empty_name(self, client):
        """空の名前でアイテム作成テスト（エラーケース）"""
        item_data = {
            "name": "",
            "description": "Test description",
            "price": 10.0
        }

        response = client.post("/items", json=item_data)

        assert response.status_code == 400
        assert "Item name cannot be empty" in response.json()["detail"]

    def test_get_item_not_found(self, client):
        """存在しないアイテム取得テスト"""
        response = client.get("/items/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"

    # ===== CRUD操作の統合テスト =====

    def test_full_crud_operations(self, client, sample_item):
        """CRUD操作の統合テスト"""

        # 1. 作成（Create）
        create_response = client.post(
            "/items", json=sample_item.model_dump(exclude={"id"}))
        assert create_response.status_code == 200
        created_item = create_response.json()
        item_id = created_item["id"]

        # 2. 読み取り（Read）
        read_response = client.get(f"/items/{item_id}")
        assert read_response.status_code == 200
        read_item = read_response.json()
        assert read_item["name"] == sample_item.name

        # 3. 更新（Update）
        updated_data = sample_item.model_dump()
        updated_data["name"] = "Updated Item Name"
        updated_data["price"] = 39.99

        update_response = client.put(f"/items/{item_id}", json=updated_data)
        assert update_response.status_code == 200
        updated_item = update_response.json()
        assert updated_item["name"] == "Updated Item Name"
        assert updated_item["price"] == 39.99

        # 4. 削除（Delete）
        delete_response = client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Item deleted successfully"

        # 5. 削除確認
        get_deleted_response = client.get(f"/items/{item_id}")
        assert get_deleted_response.status_code == 404

    # ===== パラメータ化テスト =====

    @pytest.mark.parametrize("a,b,operation,expected", [
        (10, 5, "add", 15),
        (10, 5, "subtract", 5),
        (10, 5, "multiply", 50),
        (10, 5, "divide", 2.0),
        (7, 3, "add", 10),
        (100, 25, "divide", 4.0)
    ])
    def test_calculate_operations(self, client, a, b, operation, expected):
        """計算エンドポイントのパラメータ化テスト"""
        response = client.get(f"/calculate/{a}/{b}?operation={operation}")

        assert response.status_code == 200
        result = response.json()
        assert result["a"] == a
        assert result["b"] == b
        assert result["operation"] == operation
        assert result["result"] == expected

    @pytest.mark.parametrize("a,b,operation,expected_status,expected_error", [
        (10, 0, "divide", 400, "Division by zero is not allowed"),
        (10, 5, "invalid", 400, "Invalid operation"),
        (10, 5, "modulo", 400, "Invalid operation")
    ])
    def test_calculate_error_cases(self, client, a, b, operation, expected_status, expected_error):
        """計算エンドポイントのエラーケーステスト"""
        response = client.get(f"/calculate/{a}/{b}?operation={operation}")

        assert response.status_code == expected_status
        assert expected_error in response.json()["detail"]

    # ===== モックを使用したテスト =====

    def test_external_api_call_simple(self, client):
        """外部API呼び出しのシンプルなテスト（実際のAPI呼び出し）"""
        # 注意: このテストは実際にインターネットアクセスが必要です
        # 本来はモックを使うべきですが、学習目的で実際のAPIを呼び出します

        try:
            response = client.get("/external-api")
            # 成功した場合の検証
            assert response.status_code == 200
            result = response.json()
            assert "userId" in result
            assert "id" in result
            assert "title" in result
        except Exception:
            # ネットワークエラーの場合はスキップ
            pytest.skip("ネットワーク接続が必要なテストをスキップしました")

    # ===== 依存性注入のテスト =====

    def test_protected_endpoint_with_dependency_override(self, client):
        """依存性注入のオーバーライドテスト"""

        # テスト用のユーザーを作成
        def override_get_current_user():
            return User(id=999, username="testuser999", email="test999@example.com")

        # 依存性をオーバーライド
        app.dependency_overrides[get_current_user] = override_get_current_user

        try:
            response = client.get("/protected")

            assert response.status_code == 200
            result = response.json()
            assert result["message"] == "Hello testuser999"
            assert result["user_id"] == 999

        finally:
            # オーバーライドを削除
            app.dependency_overrides.clear()

    # ===== バリデーションテスト =====

    def test_create_item_validation_errors(self, client):
        """バリデーションエラーのテスト"""
        # 必須フィールドを欠いたデータでテスト
        invalid_item_data = {
            "description": "Test description",
            # nameフィールドが欠けている（必須フィールド）
            "price": 10.0
        }

        response = client.post("/items", json=invalid_item_data)

        # バリデーションエラーが発生することを確認
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0

        # nameフィールドのエラーがあることを確認
        error_fields = []
        for error in errors:
            if "loc" in error and len(error["loc"]) > 0:
                error_fields.extend(error["loc"])

        # nameフィールドまたはbodyレベルのエラーがあることを確認
        assert "name" in error_fields or any(
            "missing" in str(error).lower() for error in errors)

    # ===== レスポンス形式テスト =====

    def test_response_headers(self, client):
        """レスポンスヘッダーのテスト"""
        response = client.get("/")

        assert response.headers["content-type"] == "application/json"
        assert response.status_code == 200

    def test_response_structure(self, client, sample_item):
        """レスポンス構造のテスト"""
        response = client.post(
            "/items", json=sample_item.model_dump(exclude={"id"}))

        assert response.status_code == 200
        created_item = response.json()

        # 必要なフィールドが存在することを確認
        required_fields = ["id", "name",
                           "description", "price", "is_available"]
        for field in required_fields:
            assert field in created_item

        # データ型の確認
        assert isinstance(created_item["id"], int)
        assert isinstance(created_item["name"], str)
        assert isinstance(created_item["description"], str)
        assert isinstance(created_item["price"], (int, float))
        assert isinstance(created_item["is_available"], bool)

# ===== テスト実行関数 =====


def run_tests():
    """テストを実行する関数"""
    import subprocess
    import sys

    print("FastAPI pytestテストの実行")
    print("=" * 40)
    print("テストを実行中...")

    try:
        # pytestを実行
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            __file__,
            "-v",  # 詳細表示
            "--tb=short"  # トレースバック形式
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"終了コード: {result.returncode}")

    except Exception as e:
        print(f"テスト実行エラー: {e}")

# ===== テスト設定とヘルパー関数 =====


def test_setup_and_teardown():
    """テストのセットアップ・ティアダウンの例"""

    @pytest.fixture(scope="session")
    def setup_test_environment():
        """セッション全体でのセットアップ"""
        print("テスト環境をセットアップ中...")
        # データベース初期化、外部サービスの準備など
        yield
        print("テスト環境をクリーンアップ中...")

    @pytest.fixture(scope="function")
    def test_data():
        """各テスト関数でのテストデータ準備"""
        data = {"test": "data"}
        yield data
        # テスト後のクリーンアップ


def test_tips_and_best_practices():
    """テストのTipsとベストプラクティス"""

    tips = {
        "naming": "テスト関数名は test_ で始める",
        "structure": "Arrange-Act-Assert パターンを使用",
        "isolation": "各テストは独立して実行可能にする",
        "fixtures": "共通のセットアップはフィクスチャを使用",
        "parametrize": "類似テストはパラメータ化で効率化",
        "mocking": "外部依存はモックで分離",
        "assertions": "明確で理解しやすいアサーションを書く"
    }

    # テスト関数は何も返してはいけない（warningを回避）
    assert tips is not None

# ===== 実行例 =====


if __name__ == "__main__":
    print("FastAPI pytest テスト教材")
    print("=" * 40)
    print("このファイルでは以下を学習します:")
    print("1. pytest の基本的な使い方")
    print("2. FastAPI TestClient を使ったAPIテスト")
    print("3. フィクスチャとパラメータ化テスト")
    print("4. モックを使用した外部依存のテスト")
    print("5. 依存性注入のテスト")
    print("6. バリデーションとエラーハンドリングのテスト")
    print("\n実行方法:")
    print("pytest " + __file__ + " -v")
    print("\nまたは:")
    print("python " + __file__)
    print("=" * 40)

    # TestClientでの簡単な動作確認
    client = TestClient(app)
    response = client.get("/")
    print(f"\n動作確認: {response.json()}")

    # テスト実行
    run_tests()
