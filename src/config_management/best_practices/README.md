# 環境変数・設定管理のベストプラクティス

## 1. セキュリティのベストプラクティス

### 🔒 機密情報の管理

#### DO（推奨）

```python
# 環境変数から機密情報を取得
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

#### DON'T（非推奨）

```python
# コードにハードコーディング
DATABASE_URL = "postgresql://user:password@localhost/db"
SECRET_KEY = "my-secret-key-123"
```

### 🔐 .env ファイルの管理

#### DO（推奨）

- `.env` ファイルを `.gitignore` に追加
- `.env.example` ファイルでテンプレートを提供
- 機密情報を含まない設定例のみを提供

```bash
# .gitignore
.env
.env.local
.env.production
```

```bash
# .env.example
DATABASE_URL=postgresql://user:password@localhost/myapp
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

#### DON'T（非推奨）

- `.env` ファイルをバージョン管理に含める
- 機密情報を含む設定をコミットする

## 2. 環境変数の命名規則

### 🏷️ 命名規則

#### DO（推奨）

```bash
# 大文字・アンダースコア区切り
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
MAX_CONNECTIONS=100
LOG_LEVEL=INFO

# プレフィックスで分類
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp

REDIS_URL=redis://localhost:6379
REDIS_MAX_CONNECTIONS=10
```

#### DON'T（非推奨）

```bash
# 小文字・大文字混在
databaseUrl=postgresql://...
jwtSecretKey=...
maxConnections=100

# 曖昧な名前
SECRET=...
URL=...
HOST=...
```

## 3. 設定の構造化

### 📁 設定クラスの分離

#### DO（推奨）

```python
class DatabaseSettings(BaseSettings):
    url: str
    pool_size: int = 10
    echo: bool = False

    class Config:
        env_prefix = "DB_"

class RedisSettings(BaseSettings):
    url: str
    max_connections: int = 10

    class Config:
        env_prefix = "REDIS_"

class AppSettings(BaseSettings):
    name: str
    version: str
    debug: bool = False

    # ネストした設定
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
```

#### DON'T（非推奨）

```python
class Settings(BaseSettings):
    # すべての設定を一つのクラスに詰め込む
    app_name: str
    app_version: str
    debug: bool
    database_url: str
    database_pool_size: int
    redis_url: str
    redis_max_connections: int
    # ... 多数の設定項目
```

## 4. 環境別設定管理

### 🌍 環境の分離

#### DO（推奨）

```python
def create_settings_for_environment(env: str) -> AppSettings:
    """環境に応じた設定を作成"""
    env_file = f".env.{env}"

    if os.path.exists(env_file):
        return AppSettings(_env_file=env_file)
    else:
        # 環境変数から設定を読み込み
        os.environ.setdefault("ENVIRONMENT", env)
        return AppSettings()

# 使用例
dev_settings = create_settings_for_environment("development")
prod_settings = create_settings_for_environment("production")
```

#### DON'T（非推奨）

```python
# 環境による条件分岐を設定クラス内に含める
class Settings(BaseSettings):
    def __init__(self):
        if os.getenv("ENVIRONMENT") == "production":
            self.debug = False
            self.log_level = "ERROR"
        else:
            self.debug = True
            self.log_level = "DEBUG"
```

## 5. バリデーションとエラーハンドリング

### ✅ 設定のバリデーション

#### DO（推奨）

```python
class AppSettings(BaseSettings):
    port: int = Field(ge=1, le=65535, description="サーバーポート")
    log_level: str = Field(description="ログレベル")
    environment: str = Field(description="実行環境")

    @field_validator('log_level')
    def validate_log_level(cls, v):
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed_levels:
            raise ValueError(f'Log level must be one of {allowed_levels}')
        return v.upper()

    @field_validator('environment')
    def validate_environment(cls, v):
        allowed_envs = ['development', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'Environment must be one of {allowed_envs}')
        return v
```

#### DON'T（非推奨）

```python
# バリデーションなしで設定を使用
class Settings(BaseSettings):
    port: int
    log_level: str
    environment: str

# バリデーションエラーを無視
try:
    settings = Settings()
except ValidationError:
    pass  # エラーを無視
```

## 6. 依存性注入パターン

### 🔄 設定の依存性注入

#### DO（推奨）

```python
# グローバル設定インスタンス
_settings: Optional[AppSettings] = None

def get_settings() -> AppSettings:
    """設定を取得（依存性注入用）"""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings

# FastAPIでの使用
@app.get("/api/data")
async def get_data(settings: AppSettings = Depends(get_settings)):
    # 設定を使用
    return {"debug": settings.debug}
```

#### DON'T（非推奨）

```python
# グローバル設定インスタンス
settings = AppSettings()

@app.get("/api/data")
async def get_data():
    # グローバル変数を直接使用
    return {"debug": settings.debug}
```

## 7. テストでの設定管理

### 🧪 テスト用設定

#### DO（推奨）

```python
@pytest.fixture
def test_settings():
    """テスト用設定"""
    return AppSettings(
        debug=True,
        environment="test",
        database_url="sqlite:///:memory:",
        redis_url="redis://localhost:6379/15"  # テスト用DB
    )

def test_api_endpoint(test_settings):
    """設定を使用したテスト"""
    app = create_app(test_settings)
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
```

#### DON'T（非推奨）

```python
def test_api_endpoint():
    """本番設定を使用したテスト"""
    # 本番設定を使用してテストを実行
    response = client.get("/health")
    assert response.status_code == 200
```

## 8. 本番環境での設定管理

### 🏭 本番環境でのベストプラクティス

#### DO（推奨）

```bash
# 環境変数で機密情報を設定
export DATABASE_URL="postgresql://user:password@host:5432/db"
export SECRET_KEY="$(openssl rand -base64 32)"
export JWT_SECRET_KEY="$(openssl rand -base64 32)"

# Docker環境
docker run -e DATABASE_URL="postgresql://..." myapp

# Kubernetes環境
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
data:
  database-url: <base64-encoded-url>
  secret-key: <base64-encoded-secret>
```

#### DON'T（非推奨）

```bash
# .envファイルを本番環境で使用
# 機密情報をプレーンテキストで保存
```

## 9. ログとモニタリング

### 📊 設定の監視

#### DO（推奨）

```python
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の設定確認"""
    settings = get_settings()

    logger.info(f"Starting {settings.name} v{settings.version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # 重要な設定値の確認
    if settings.environment == "production":
        if settings.debug:
            logger.warning("Debug mode is enabled in production!")
        if "localhost" in settings.security.allowed_hosts:
            logger.warning("Localhost is allowed in production!")
```

#### DON'T（非推奨）

```python
# 設定の確認やログ出力なし
@app.on_event("startup")
async def startup_event():
    pass
```

## 10. ドキュメント化

### 📝 設定のドキュメント

#### DO（推奨）

```python
class AppSettings(BaseSettings):
    """アプリケーション設定

    環境変数またはresource ファイルから設定を読み込みます。
    """

    database_url: str = Field(
        default="sqlite:///./app.db",
        description="データベース接続URL。PostgreSQL推奨",
        env="DATABASE_URL"
    )

    debug: bool = Field(
        default=False,
        description="デバッグモード。本番環境では False にする",
        env="DEBUG"
    )
```

#### DON'T（非推奨）

```python
class AppSettings(BaseSettings):
    database_url: str
    debug: bool
    # ドキュメント化なし
```

## まとめ

1. **セキュリティファースト**: 機密情報を適切に管理する
2. **環境分離**: 開発・ステージング・本番環境を明確に分ける
3. **バリデーション**: 設定値を検証してエラーを防ぐ
4. **構造化**: 設定を論理的にグループ化する
5. **テスト可能**: テスト用設定を用意する
6. **ドキュメント化**: 設定項目を明確に説明する
7. **監視**: 設定の変更を追跡する
8. **自動化**: 設定の展開を自動化する
