# FastAPI テスト開発実践演習

## 🎯 目標

FastAPIアプリケーションのテスト開発技術を段階的に習得し、実際のプロジェクトで活用できるテスト戦略を身につける

---

## 演習1: 基本的なAPIテスト（入門）

### 目標
FastAPIのTestClientを使った基本的なテストの書き方を学ぶ

### 課題内容

1. **シンプルなAPIのテスト**
   - GETエンドポイントのテスト
   - POSTエンドポイントのテスト
   - エラーケースのテスト

2. **テストの基本構造**
   - テストファイルの構成
   - アサーションの書き方

### ファイル構成
```
exercise1/
├── main.py          # FastAPIアプリ
├── test_basic.py    # 基本テスト
└── requirements.txt
```

### 実装例

**main.py**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# インメモリデータストレージ
items_db = {}
next_id = 1

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class ItemResponse(Item):
    id: int

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items", response_model=List[ItemResponse])
def read_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    global next_id
    item_data = item.dict()
    item_data["id"] = next_id
    items_db[next_id] = item_data
    next_id += 1
    return item_data

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.dict()
    item_data["id"] = item_id
    items_db[item_id] = item_data
    return item_data

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_db[item_id]
    return {"message": "Item deleted"}
```

**test_basic.py**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

# TestClientの作成
client = TestClient(app)

class TestBasicAPI:
    """基本的なAPIテスト"""
    
    def test_read_root(self):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
    
    def test_create_item(self):
        """アイテム作成のテスト"""
        item_data = {
            "name": "Test Item",
            "description": "A test item",
            "price": 10.5,
            "tax": 1.5
        }
        
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["name"] == item_data["name"]
        assert response_data["price"] == item_data["price"]
        assert "id" in response_data
    
    def test_read_items(self):
        """アイテム一覧取得のテスト"""
        # まずアイテムを作成
        item_data = {
            "name": "Test Item 2",
            "price": 20.0
        }
        client.post("/items", json=item_data)
        
        # アイテム一覧を取得
        response = client.get("/items")
        assert response.status_code == 200
        
        items = response.json()
        assert isinstance(items, list)
        assert len(items) > 0
    
    def test_read_item_by_id(self):
        """ID指定でのアイテム取得テスト"""
        # アイテム作成
        item_data = {
            "name": "Test Item 3",
            "price": 30.0
        }
        create_response = client.post("/items", json=item_data)
        created_item = create_response.json()
        item_id = created_item["id"]
        
        # ID指定で取得
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        
        item = response.json()
        assert item["id"] == item_id
        assert item["name"] == item_data["name"]
    
    def test_update_item(self):
        """アイテム更新のテスト"""
        # アイテム作成
        item_data = {
            "name": "Original Item",
            "price": 40.0
        }
        create_response = client.post("/items", json=item_data)
        created_item = create_response.json()
        item_id = created_item["id"]
        
        # アイテム更新
        updated_data = {
            "name": "Updated Item",
            "price": 45.0,
            "description": "Updated description"
        }
        
        response = client.put(f"/items/{item_id}", json=updated_data)
        assert response.status_code == 200
        
        updated_item = response.json()
        assert updated_item["name"] == updated_data["name"]
        assert updated_item["price"] == updated_data["price"]
        assert updated_item["description"] == updated_data["description"]
    
    def test_delete_item(self):
        """アイテム削除のテスト"""
        # アイテム作成
        item_data = {
            "name": "Item to Delete",
            "price": 50.0
        }
        create_response = client.post("/items", json=item_data)
        created_item = create_response.json()
        item_id = created_item["id"]
        
        # アイテム削除
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        
        # 削除されたことを確認
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

class TestErrorCases:
    """エラーケースのテスト"""
    
    def test_get_nonexistent_item(self):
        """存在しないアイテムの取得テスト"""
        response = client.get("/items/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
    
    def test_update_nonexistent_item(self):
        """存在しないアイテムの更新テスト"""
        item_data = {
            "name": "Non-existent Item",
            "price": 60.0
        }
        
        response = client.put("/items/999999", json=item_data)
        assert response.status_code == 404
    
    def test_delete_nonexistent_item(self):
        """存在しないアイテムの削除テスト"""
        response = client.delete("/items/999999")
        assert response.status_code == 404
    
    def test_invalid_item_data(self):
        """無効なデータでのアイテム作成テスト"""
        invalid_data = {
            "name": "Invalid Item",
            "price": "not_a_number"  # 数値でない価格
        }
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422  # Validation Error
```

### 実行方法
```bash
# テスト実行
pytest test_basic.py -v

# カバレッジ付きでテスト実行
pytest test_basic.py --cov=main --cov-report=html
```

### チェックポイント
- [ ] 全てのテストがパスする
- [ ] 正常ケースとエラーケースがテストされている
- [ ] レスポンスの形式が正しく検証されている
- [ ] HTTPステータスコードが適切にチェックされている

---

## 演習2: データベースを使ったテスト（初級〜中級）

### 目標
SQLAlchemyを使ったアプリケーションのテスト方法を学ぶ

### 課題内容

1. **テスト用データベースの設定**
   - インメモリSQLiteの使用
   - テストフィクスチャの作成

2. **データベーステストの実装**
   - CRUD操作のテスト
   - トランザクションのテスト

### 追加ファイル

**database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# テスト環境かどうかを判定
TESTING = os.getenv("TESTING", False)

if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**models.py**
```python
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    tax = Column(Float)
```

**main_with_db.py**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db, engine, Base
import models

# テーブル作成
Base.metadata.create_all(bind=engine)

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class ItemResponse(ItemCreate):
    id: int
    
    class Config:
        from_attributes = True

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}
```

**test_database.py**
```python
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# テスト環境を設定
os.environ["TESTING"] = "True"

from main_with_db import app, get_db
from database import Base
import models

# テスト用データベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    """テスト用データベースセッション"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """テストクライアント"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

class TestDatabaseAPI:
    """データベースAPIのテスト"""
    
    def test_create_and_read_item(self, client):
        """アイテム作成と読み取りのテスト"""
        # アイテム作成
        item_data = {
            "name": "Test Item",
            "description": "A test item",
            "price": 10.5,
            "tax": 1.5
        }
        
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        
        created_item = response.json()
        assert created_item["name"] == item_data["name"]
        assert created_item["id"] == 1
        
        # アイテム読み取り
        response = client.get(f"/items/{created_item['id']}")
        assert response.status_code == 200
        
        retrieved_item = response.json()
        assert retrieved_item == created_item
    
    def test_list_items(self, client):
        """アイテム一覧取得のテスト"""
        # 複数アイテム作成
        items_data = [
            {"name": "Item 1", "price": 10.0},
            {"name": "Item 2", "price": 20.0},
            {"name": "Item 3", "price": 30.0}
        ]
        
        created_items = []
        for item_data in items_data:
            response = client.post("/items", json=item_data)
            created_items.append(response.json())
        
        # 一覧取得
        response = client.get("/items")
        assert response.status_code == 200
        
        items = response.json()
        assert len(items) == 3
        
        # 各アイテムが含まれていることを確認
        for created_item in created_items:
            assert created_item in items
    
    def test_update_item(self, client):
        """アイテム更新のテスト"""
        # アイテム作成
        item_data = {
            "name": "Original Item",
            "price": 40.0
        }
        
        response = client.post("/items", json=item_data)
        created_item = response.json()
        item_id = created_item["id"]
        
        # アイテム更新
        updated_data = {
            "name": "Updated Item",
            "price": 45.0,
            "description": "Updated description"
        }
        
        response = client.put(f"/items/{item_id}", json=updated_data)
        assert response.status_code == 200
        
        updated_item = response.json()
        assert updated_item["name"] == updated_data["name"]
        assert updated_item["price"] == updated_data["price"]
        assert updated_item["description"] == updated_data["description"]
        assert updated_item["id"] == item_id
    
    def test_delete_item(self, client):
        """アイテム削除のテスト"""
        # アイテム作成
        item_data = {
            "name": "Item to Delete",
            "price": 50.0
        }
        
        response = client.post("/items", json=item_data)
        created_item = response.json()
        item_id = created_item["id"]
        
        # アイテム削除
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        
        # 削除されたことを確認
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 404
    
    def test_database_persistence(self, db_session):
        """データベースの永続性テスト"""
        # 直接データベースにアイテム作成
        db_item = models.Item(
            name="Direct DB Item",
            description="Created directly in DB",
            price=100.0,
            tax=10.0
        )
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)
        
        # データベースから読み取り
        retrieved_item = db_session.query(models.Item).filter(
            models.Item.id == db_item.id
        ).first()
        
        assert retrieved_item is not None
        assert retrieved_item.name == "Direct DB Item"
        assert retrieved_item.price == 100.0
```

### チェックポイント
- [ ] テスト用データベースが正しく設定されている
- [ ] 各テストが独立して実行される
- [ ] データベースの状態がテスト間で影響し合わない
- [ ] 直接的なデータベース操作もテストされている

---

## 演習3: モックとスタブを使ったテスト（中級）

### 目標
外部依存関係をモック化したテストの書き方を学ぶ

### 課題内容

1. **外部APIのモック化**
   - HTTPクライアントのモック
   - レスポンスの制御

2. **データベース操作のモック化**
   - 特定の条件でのテスト

### 実装例

**external_service.py**
```python
import httpx
from typing import Dict, Any

class ExternalAPIService:
    """外部API呼び出しサービス"""
    
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
    
    async def get_item_info(self, item_name: str) -> Dict[str, Any]:
        """外部APIからアイテム情報を取得"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/items/{item_name}")
            response.raise_for_status()
            return response.json()
    
    async def validate_item_name(self, item_name: str) -> bool:
        """外部APIでアイテム名の妥当性を検証"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/validate/{item_name}")
                return response.status_code == 200
        except httpx.HTTPError:
            return False
```

**main_with_external.py**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from external_service import ExternalAPIService

app = FastAPI()

def get_external_service():
    return ExternalAPIService()

@app.post("/items/enhanced")
async def create_enhanced_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    external_service: ExternalAPIService = Depends(get_external_service)
):
    """外部API連携付きアイテム作成"""
    
    # 外部APIでアイテム名を検証
    is_valid = await external_service.validate_item_name(item.name)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid item name")
    
    # 外部APIから追加情報を取得
    try:
        external_info = await external_service.get_item_info(item.name)
        # 外部情報を商品情報に反映
        if "suggested_price" in external_info:
            item.price = external_info["suggested_price"]
    except Exception:
        # 外部API呼び出し失敗時はそのまま処理続行
        pass
    
    # データベースに保存
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item
```

**test_mocking.py**
```python
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main_with_external import app, get_external_service
from external_service import ExternalAPIService

class TestMocking:
    """モックを使ったテスト"""
    
    @pytest.fixture
    def mock_external_service(self):
        """外部サービスのモック"""
        mock_service = AsyncMock(spec=ExternalAPIService)
        return mock_service
    
    def test_create_enhanced_item_with_valid_name(self, client, mock_external_service):
        """有効なアイテム名での作成テスト"""
        # モックの設定
        mock_external_service.validate_item_name.return_value = True
        mock_external_service.get_item_info.return_value = {
            "suggested_price": 25.0,
            "category": "electronics"
        }
        
        # 依存性注入をオーバーライド
        app.dependency_overrides[get_external_service] = lambda: mock_external_service
        
        try:
            item_data = {
                "name": "Valid Item",
                "price": 10.0
            }
            
            response = client.post("/items/enhanced", json=item_data)
            assert response.status_code == 200
            
            created_item = response.json()
            assert created_item["name"] == "Valid Item"
            assert created_item["price"] == 25.0  # 外部APIの推奨価格が適用される
            
            # モックが呼ばれたことを確認
            mock_external_service.validate_item_name.assert_called_once_with("Valid Item")
            mock_external_service.get_item_info.assert_called_once_with("Valid Item")
        
        finally:
            # オーバーライドをクリア
            app.dependency_overrides = {}
    
    def test_create_enhanced_item_with_invalid_name(self, client, mock_external_service):
        """無効なアイテム名での作成テスト"""
        # モックの設定
        mock_external_service.validate_item_name.return_value = False
        
        app.dependency_overrides[get_external_service] = lambda: mock_external_service
        
        try:
            item_data = {
                "name": "Invalid Item",
                "price": 10.0
            }
            
            response = client.post("/items/enhanced", json=item_data)
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid item name"
            
            # 検証のみ呼ばれ、情報取得は呼ばれないことを確認
            mock_external_service.validate_item_name.assert_called_once_with("Invalid Item")
            mock_external_service.get_item_info.assert_not_called()
        
        finally:
            app.dependency_overrides = {}
    
    @patch('external_service.httpx.AsyncClient')
    async def test_external_service_with_patch(self, mock_client):
        """httpxクライアントを直接モック化"""
        # モックレスポンスの設定
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"valid": True}
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # テスト実行
        service = ExternalAPIService()
        result = await service.get_item_info("test_item")
        
        assert result == {"valid": True}
        mock_client_instance.get.assert_called_once_with(
            "https://api.example.com/items/test_item"
        )
    
    def test_with_database_mock(self, client):
        """データベース操作のモック化"""
        with patch('models.Item') as mock_item_class:
            # モックインスタンスの設定
            mock_item = AsyncMock()
            mock_item.id = 1
            mock_item.name = "Mocked Item"
            mock_item.price = 15.0
            
            mock_item_class.return_value = mock_item
            
            # セッションのモック化も必要な場合
            with patch('main_with_external.get_db') as mock_get_db:
                mock_db = AsyncMock()
                mock_get_db.return_value = mock_db
                
                # テストの実行...
                # （実際の実装では、より詳細なモック設定が必要）
```

### チェックポイント
- [ ] 外部依存関係が適切にモック化されている
- [ ] モックの戻り値が期待通りに設定されている
- [ ] モックが期待した回数だけ呼ばれることが確認されている
- [ ] 異常系の動作もテストされている

---

## 演習4: パフォーマンステスト（中級〜上級）

### 目標
負荷テストとパフォーマンス測定の技術を学ぶ

### 課題内容

1. **レスポンス時間のテスト**
   - 個別エンドポイントの性能測定
   - ベンチマークテスト

2. **負荷テスト**
   - 同時接続数のテスト
   - スループットの測定

### 実装例

**test_performance.py**
```python
import pytest
import time
import asyncio
import concurrent.futures
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestPerformance:
    """パフォーマンステスト"""
    
    def test_response_time_single_request(self):
        """単一リクエストのレスポンス時間テスト"""
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # 1秒以内にレスポンス
    
    def test_average_response_time(self):
        """平均レスポンス時間テスト"""
        times = []
        num_requests = 100
        
        for _ in range(num_requests):
            start_time = time.time()
            response = client.get("/")
            end_time = time.time()
            
            assert response.status_code == 200
            times.append(end_time - start_time)
        
        average_time = sum(times) / len(times)
        max_time = max(times)
        
        assert average_time < 0.1  # 平均100ms以内
        assert max_time < 0.5     # 最大500ms以内
        
        print(f"Average response time: {average_time:.4f}s")
        print(f"Max response time: {max_time:.4f}s")
    
    def test_concurrent_requests(self):
        """同時リクエストのテスト"""
        def make_request():
            start_time = time.time()
            response = client.get("/")
            end_time = time.time()
            return response.status_code, end_time - start_time
        
        # 10個の同時リクエスト
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # 全リクエストが成功することを確認
        for status_code, response_time in results:
            assert status_code == 200
            assert response_time < 2.0  # 負荷時でも2秒以内
    
    def test_database_performance(self):
        """データベース操作のパフォーマンステスト"""
        # 大量データの作成
        items_data = [
            {
                "name": f"Performance Test Item {i}",
                "price": float(i),
                "description": f"Description {i}"
            }
            for i in range(100)
        ]
        
        # 作成時間の測定
        start_time = time.time()
        created_items = []
        
        for item_data in items_data:
            response = client.post("/items", json=item_data)
            assert response.status_code == 200
            created_items.append(response.json())
        
        creation_time = time.time() - start_time
        
        # 読み取り時間の測定
        start_time = time.time()
        response = client.get("/items")
        read_time = time.time() - start_time
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) >= 100
        
        print(f"Creation time for 100 items: {creation_time:.4f}s")
        print(f"Read time for items list: {read_time:.4f}s")
        
        # パフォーマンス基準
        assert creation_time < 10.0  # 100件作成で10秒以内
        assert read_time < 1.0       # 読み取りで1秒以内

@pytest.mark.asyncio
class TestAsyncPerformance:
    """非同期パフォーマンステスト"""
    
    async def test_async_concurrent_requests(self):
        """非同期での同時リクエストテスト"""
        import httpx
        
        async def make_async_request(client):
            start_time = time.time()
            response = await client.get("http://testserver/")
            end_time = time.time()
            return response.status_code, end_time - start_time
        
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as async_client:
            # 50個の同時非同期リクエスト
            tasks = [make_async_request(async_client) for _ in range(50)]
            results = await asyncio.gather(*tasks)
        
        # 全リクエストが成功することを確認
        for status_code, response_time in results:
            assert status_code == 200
            assert response_time < 5.0  # 非同期でも5秒以内
        
        # 統計情報
        response_times = [result[1] for result in results]
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        print(f"Async average response time: {avg_time:.4f}s")
        print(f"Async max response time: {max_time:.4f}s")
```

### ベンチマークツールの使用例

**locust_test.py**（Locustを使った負荷テスト）
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)  # 1-3秒待機
    
    def on_start(self):
        """テスト開始時の初期化"""
        self.item_ids = []
    
    @task(3)  # 重み付け：3回に1回実行
    def get_root(self):
        """ルートエンドポイントのテスト"""
        self.client.get("/")
    
    @task(2)
    def create_item(self):
        """アイテム作成のテスト"""
        item_data = {
            "name": f"Load Test Item {len(self.item_ids)}",
            "price": 10.0
        }
        
        response = self.client.post("/items", json=item_data)
        if response.status_code == 200:
            item_id = response.json()["id"]
            self.item_ids.append(item_id)
    
    @task(1)
    def get_item(self):
        """アイテム取得のテスト"""
        if self.item_ids:
            item_id = self.item_ids[-1]
            self.client.get(f"/items/{item_id}")
    
    @task(1)
    def get_items_list(self):
        """アイテム一覧取得のテスト"""
        self.client.get("/items")

# 実行コマンド:
# locust -f locust_test.py --host=http://localhost:8000
```

### チェックポイント
- [ ] レスポンス時間が期待値以内に収まる
- [ ] 同時接続時のパフォーマンスが維持される
- [ ] データベース操作のパフォーマンスが適切
- [ ] 負荷テストツールが正しく動作する

---

## 演習5: エンドツーエンド（E2E）テスト（上級）

### 目標
実際のユーザーシナリオに基づく統合テストを実装する

### 課題内容

1. **ユーザーシナリオテスト**
   - 完全なワークフローのテスト
   - 複数エンドポイントの連携

2. **データの整合性テスト**
   - 一連の操作後のデータ状態確認

### 実装例

**test_e2e.py**
```python
import pytest
from fastapi.testclient import TestClient
from main_with_db import app

client = TestClient(app)

class TestE2EScenarios:
    """エンドツーエンドシナリオテスト"""
    
    def test_complete_item_lifecycle(self):
        """アイテムの完全なライフサイクルテスト"""
        
        # 1. アイテム作成
        item_data = {
            "name": "E2E Test Item",
            "description": "An item for end-to-end testing",
            "price": 25.99,
            "tax": 2.60
        }
        
        create_response = client.post("/items", json=item_data)
        assert create_response.status_code == 200
        
        created_item = create_response.json()
        item_id = created_item["id"]
        
        # 作成されたアイテムの検証
        assert created_item["name"] == item_data["name"]
        assert created_item["price"] == item_data["price"]
        
        # 2. アイテム読み取り
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        
        retrieved_item = get_response.json()
        assert retrieved_item == created_item
        
        # 3. アイテム一覧に含まれていることを確認
        list_response = client.get("/items")
        assert list_response.status_code == 200
        
        items_list = list_response.json()
        assert any(item["id"] == item_id for item in items_list)
        
        # 4. アイテム更新
        updated_data = {
            "name": "Updated E2E Test Item",
            "description": "Updated description",
            "price": 30.99,
            "tax": 3.10
        }
        
        update_response = client.put(f"/items/{item_id}", json=updated_data)
        assert update_response.status_code == 200
        
        updated_item = update_response.json()
        assert updated_item["name"] == updated_data["name"]
        assert updated_item["price"] == updated_data["price"]
        assert updated_item["id"] == item_id
        
        # 5. 更新が反映されていることを確認
        get_updated_response = client.get(f"/items/{item_id}")
        assert get_updated_response.status_code == 200
        
        final_item = get_updated_response.json()
        assert final_item["name"] == updated_data["name"]
        
        # 6. アイテム削除
        delete_response = client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200
        
        # 7. 削除されたことを確認
        get_deleted_response = client.get(f"/items/{item_id}")
        assert get_deleted_response.status_code == 404
        
        # 8. 一覧からも削除されていることを確認
        final_list_response = client.get("/items")
        final_items_list = final_list_response.json()
        assert not any(item["id"] == item_id for item in final_items_list)
    
    def test_multiple_items_workflow(self):
        """複数アイテムのワークフローテスト"""
        
        # 複数のアイテムを作成
        items_data = [
            {"name": "Item A", "price": 10.0},
            {"name": "Item B", "price": 20.0},
            {"name": "Item C", "price": 30.0}
        ]
        
        created_items = []
        for item_data in items_data:
            response = client.post("/items", json=item_data)
            assert response.status_code == 200
            created_items.append(response.json())
        
        # 全てのアイテムが一覧に含まれていることを確認
        list_response = client.get("/items")
        items_list = list_response.json()
        
        for created_item in created_items:
            assert any(
                item["id"] == created_item["id"] and 
                item["name"] == created_item["name"]
                for item in items_list
            )
        
        # 偶数IDのアイテムを削除
        for created_item in created_items:
            if created_item["id"] % 2 == 0:
                delete_response = client.delete(f"/items/{created_item['id']}")
                assert delete_response.status_code == 200
        
        # 削除後の一覧を確認
        final_list_response = client.get("/items")
        final_items_list = final_list_response.json()
        
        for created_item in created_items:
            if created_item["id"] % 2 == 0:
                # 偶数IDは削除されている
                assert not any(item["id"] == created_item["id"] for item in final_items_list)
            else:
                # 奇数IDは残っている
                assert any(item["id"] == created_item["id"] for item in final_items_list)
    
    def test_error_recovery_scenario(self):
        """エラー回復シナリオのテスト"""
        
        # 1. 正常なアイテム作成
        valid_item = {
            "name": "Valid Item",
            "price": 15.0
        }
        
        create_response = client.post("/items", json=valid_item)
        assert create_response.status_code == 200
        created_item = create_response.json()
        item_id = created_item["id"]
        
        # 2. 無効なデータで更新を試行（エラーが発生）
        invalid_update = {
            "name": "Updated Item",
            "price": "invalid_price"  # 無効な価格
        }
        
        update_response = client.put(f"/items/{item_id}", json=invalid_update)
        assert update_response.status_code == 422  # Validation Error
        
        # 3. 元のデータが変更されていないことを確認
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        
        unchanged_item = get_response.json()
        assert unchanged_item["name"] == valid_item["name"]
        assert unchanged_item["price"] == valid_item["price"]
        
        # 4. 正しいデータで再度更新
        valid_update = {
            "name": "Correctly Updated Item",
            "price": 20.0
        }
        
        correct_update_response = client.put(f"/items/{item_id}", json=valid_update)
        assert correct_update_response.status_code == 200
        
        # 5. 更新が適用されていることを確認
        final_get_response = client.get(f"/items/{item_id}")
        final_item = final_get_response.json()
        assert final_item["name"] == valid_update["name"]
        assert final_item["price"] == valid_update["price"]

class TestDataConsistency:
    """データ整合性テスト"""
    
    def test_concurrent_operations_consistency(self):
        """同時操作でのデータ整合性テスト"""
        import threading
        import time
        
        results = []
        errors = []
        
        def create_item(thread_id):
            try:
                item_data = {
                    "name": f"Concurrent Item {thread_id}",
                    "price": float(thread_id)
                }
                
                response = client.post("/items", json=item_data)
                results.append((thread_id, response.status_code, response.json()))
            except Exception as e:
                errors.append((thread_id, str(e)))
        
        # 10個のスレッドで同時にアイテム作成
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_item, args=(i,))
            threads.append(thread)
        
        # 全スレッド開始
        for thread in threads:
            thread.start()
        
        # 全スレッド終了を待機
        for thread in threads:
            thread.join()
        
        # エラーがないことを確認
        assert len(errors) == 0, f"Errors occurred: {errors}"
        
        # 全ての作成が成功していることを確認
        assert len(results) == 10
        for thread_id, status_code, response_data in results:
            assert status_code == 200
            assert response_data["name"] == f"Concurrent Item {thread_id}"
        
        # データベースの整合性を確認
        list_response = client.get("/items")
        items_list = list_response.json()
        
        # 作成されたアイテムが全て存在することを確認
        for thread_id, _, created_item in results:
            assert any(
                item["id"] == created_item["id"] and 
                item["name"] == f"Concurrent Item {thread_id}"
                for item in items_list
            )
```

### チェックポイント
- [ ] 完全なユーザーワークフローがテストされている
- [ ] エラー発生時の回復シナリオがテストされている
- [ ] 同時操作でのデータ整合性が保たれている
- [ ] 複雑なシナリオでも予期した動作をする

---

## 🎯 テスト実行とレポート

### 実行コマンド集

```bash
# 基本的なテスト実行
pytest test_basic.py -v

# カバレッジレポート付き
pytest --cov=main --cov-report=html --cov-report=term

# 特定のテストクラスのみ実行
pytest test_basic.py::TestBasicAPI -v

# 並列実行（pytest-xdist使用）
pytest -n 4

# パフォーマンステストを除外
pytest -m "not performance"

# 詳細なテスト結果
pytest --tb=long --capture=no
```

### カバレッジ目標
- **関数カバレッジ**: 90%以上
- **行カバレッジ**: 85%以上
- **分岐カバレッジ**: 80%以上

### CI/CD統合例

**.github/workflows/test.yml**
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=main --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

---

## 🎓 次のステップ

これらのテスト演習を完了したら、以下の発展的なトピックに取り組むことをお勧めします：

1. **契約テスト（Contract Testing）**
   - Pact等のツールを使用

2. **セキュリティテスト**
   - 認証・認可のテスト
   - SQLインジェクション対策テスト

3. **API仕様テスト**
   - OpenAPI仕様との整合性テスト

4. **カオスエンジニアリング**
   - 障害注入テスト

各演習で学んだテスト技術を組み合わせて、より堅牢で信頼性の高いAPIを構築していきましょう！
