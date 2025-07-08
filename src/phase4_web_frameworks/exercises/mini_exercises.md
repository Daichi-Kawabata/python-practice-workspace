# FastAPI ミニ演習課題集

## 🎯 目的

総合演習に取り組む前に、個別の機能を段階的に学習・練習するためのミニ演習課題です。各課題は30分〜1時間程度で完了できる内容となっています。

---

## 演習1: シンプルなAPI作成（入門）

### 目標
FastAPIの基本的なルーティングとレスポンス形式を理解する

### 課題内容
1. 以下のエンドポイントを持つAPIを作成
   - `GET /` : "Hello, FastAPI!"を返す
   - `GET /health` : サーバーの状態をJSON形式で返す
   - `GET /users/{user_id}` : パスパラメータを受け取り、ユーザー情報を返す
   - `POST /echo` : リクエストボディをそのまま返す

### 実装例のヒント
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EchoRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

# 他のエンドポイントを実装してください
```

### チェックポイント
- [ ] Swagger UI (`/docs`) でAPIドキュメントが表示される
- [ ] 各エンドポイントが正常に動作する
- [ ] Pydanticモデルを使用したリクエスト/レスポンス定義

---

## 演習2: バリデーション強化（初級）

### 目標
Pydanticを使った入力検証とエラーハンドリングを学ぶ

### 課題内容
ユーザー情報を管理するAPIを作成：

1. **ユーザー作成** `POST /users`
   - 名前（必須、3文字以上）
   - 年齢（必須、0〜120歳）
   - メールアドレス（必須、形式チェック）

2. **ユーザー情報更新** `PUT /users/{user_id}`
   - 部分更新対応（Optional fields）

3. **バリデーションエラー時の適切なレスポンス**

### 実装のヒント
```python
from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    
    @validator('name')
    def name_must_be_long_enough(cls, v):
        if len(v) < 3:
            raise ValueError('名前は3文字以上である必要があります')
        return v
    
    @validator('age')
    def age_must_be_valid(cls, v):
        if v < 0 or v > 120:
            raise ValueError('年齢は0〜120歳である必要があります')
        return v
```

### チェックポイント
- [ ] 各フィールドのバリデーションが動作する
- [ ] エラー時に適切なHTTPステータスコードが返される
- [ ] Swagger UIでバリデーションルールが確認できる

---

## 演習3: メモリデータベース（初級〜中級）

### 目標
インメモリデータストレージを使ったCRUD操作を実装する

### 課題内容
書籍管理APIを作成：

1. **書籍一覧取得** `GET /books`
   - クエリパラメータによる検索・フィルタリング
   - ページネーション対応

2. **書籍詳細取得** `GET /books/{book_id}`

3. **書籍追加** `POST /books`

4. **書籍更新** `PUT /books/{book_id}`

5. **書籍削除** `DELETE /books/{book_id}`

### 実装のヒント
```python
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import uuid

# インメモリデータストレージ
books_db = {}

class Book(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    isbn: Optional[str] = None
    published_year: int
    genre: str

@app.get("/books", response_model=List[Book])
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None
):
    # 実装してください
    pass
```

### チェックポイント
- [ ] 全てのCRUD操作が動作する
- [ ] 適切なHTTPステータスコードが返される
- [ ] エラーハンドリングが適切に実装されている
- [ ] クエリパラメータによる検索・フィルタリングが動作する

---

## 演習4: ミドルウェア実装（中級）

### 目標
カスタムミドルウェアを作成し、リクエスト/レスポンスの処理を理解する

### 課題内容
以下のミドルウェアを実装：

1. **リクエストロギングミドルウェア**
   - リクエストURL、メソッド、処理時間をログ出力

2. **レート制限ミドルウェア**
   - 同一IPアドレスからのリクエスト数を制限

3. **リクエストIDミドルウェア**
   - 各リクエストに一意のIDを付与し、レスポンスヘッダーに含める

### 実装のヒント
```python
import time
import uuid
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # リクエスト処理
        response = await call_next(request)
        
        # 処理時間計算
        process_time = time.time() - start_time
        
        # ログ出力
        print(f"{request.method} {request.url.path} - {process_time:.4f}s")
        
        return response

# アプリケーションに追加
app.add_middleware(RequestLoggingMiddleware)
```

### チェックポイント
- [ ] リクエストログが正常に出力される
- [ ] レート制限が動作する（429 Too Many Requests）
- [ ] リクエストIDがレスポンスヘッダーに含まれる

---

## 演習5: 非同期処理実践（中級〜上級）

### 目標
非同期処理を活用した外部API連携とパフォーマンス最適化

### 課題内容
天気情報APIを作成：

1. **外部天気APIとの連携**
   - OpenWeatherMap APIなどを使用
   - 複数都市の天気情報を並行取得

2. **キャッシュ機能の実装**
   - インメモリキャッシュで重複リクエストを削減

3. **タイムアウトとエラーハンドリング**

### 実装のヒント
```python
import asyncio
import aiohttp
from fastapi import HTTPException
from typing import List

class WeatherService:
    def __init__(self):
        self.cache = {}
        self.api_key = "your_api_key"  # 実際のAPIキーを設定
    
    async def get_weather(self, city: str) -> dict:
        # キャッシュチェック
        if city in self.cache:
            return self.cache[city]
        
        # 外部API呼び出し
        async with aiohttp.ClientSession() as session:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": self.api_key}
            
            try:
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.cache[city] = data  # キャッシュ保存
                        return data
                    else:
                        raise HTTPException(status_code=404, detail="City not found")
            except asyncio.TimeoutError:
                raise HTTPException(status_code=408, detail="Request timeout")

@app.get("/weather/{city}")
async def get_weather(city: str):
    service = WeatherService()
    return await service.get_weather(city)

@app.get("/weather-multiple")
async def get_multiple_weather(cities: List[str]):
    service = WeatherService()
    tasks = [service.get_weather(city) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {"results": results}
```

### チェックポイント
- [ ] 外部APIとの非同期通信が動作する
- [ ] 複数リクエストの並行処理が実装されている
- [ ] タイムアウトとエラーハンドリングが適切に動作する
- [ ] キャッシュ機能が動作する

---

## 演習6: 簡易認証システム（中級〜上級）

### 目標
JWT認証を使ったセキュアなAPIを構築する

### 課題内容
ユーザー認証機能付きのメモAPIを作成：

1. **ユーザー登録・ログイン**
   - パスワードハッシュ化
   - JWTトークン生成

2. **認証が必要なエンドポイント**
   - メモの作成・読み取り・更新・削除
   - ユーザーは自分のメモのみアクセス可能

3. **権限管理**
   - 管理者権限の実装

### 実装のヒント
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# パスワードハッシュ化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証情報が無効です"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証情報が無効です"
        )

@app.post("/memos")
async def create_memo(memo_data: MemoCreate, current_user: str = Depends(get_current_user)):
    # 認証されたユーザーのみアクセス可能
    pass
```

### チェックポイント
- [ ] ユーザー登録・ログインが動作する
- [ ] JWTトークンが正しく生成・検証される
- [ ] 認証が必要なエンドポイントが保護されている
- [ ] ユーザーは自分のデータのみアクセス可能

---

## 🎓 次のステップ

これらのミニ演習を完了したら、`comprehensive_api_exercise.md`の総合演習課題に挑戦してください。各ミニ演習で学んだ技術を組み合わせて、より実践的なAPIを構築できるはずです。

### 追加学習リソース

1. **FastAPI公式ドキュメント**: https://fastapi.tiangolo.com/
2. **Pydanticドキュメント**: https://pydantic-docs.helpmanual.io/
3. **SQLAlchemyチュートリアル**: https://docs.sqlalchemy.org/en/14/tutorial/
4. **JWT.io**: https://jwt.io/ - JWTトークンの理解に有効

### デバッグのコツ

1. **ログ出力を活用**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   ```

2. **Swagger UIでテスト**
   - `http://localhost:8000/docs` でインタラクティブにテスト

3. **pytest でユニットテスト**
   ```python
   from fastapi.testclient import TestClient
   client = TestClient(app)
   
   def test_read_main():
       response = client.get("/")
       assert response.status_code == 200
   ```

各演習で疑問が生じた場合は、遠慮なく質問してください！
