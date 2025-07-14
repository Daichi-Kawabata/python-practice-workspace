# Docker Compose 完全ガイド - 環境変数管理とマルチコンテナ運用

## 🔍 Docker Compose とは

Docker Compose は**複数のコンテナ**を**宣言的**に管理するツールです。

### docker run vs docker-compose の違い

|                  | `docker run`   | `docker-compose`       |
| ---------------- | -------------- | ---------------------- |
| **対象**         | 単一コンテナ   | **複数コンテナ**       |
| **設定方法**     | コマンドライン | **YAML ファイル**      |
| **ネットワーク** | 手動設定       | **自動作成**           |
| **依存関係**     | 手動管理       | **自動管理**           |
| **環境管理**     | コマンドで指定 | **ファイルで管理**     |
| **用途**         | 簡単なテスト   | **本格的な開発・本番** |

## 📝 基本的な docker-compose.yml の構造

```yaml
version: "3.8"

services: # コンテナの定義
  app-dev: # サービス名
    build: . # Dockerfileからビルド
    environment: # 環境変数設定
      - APP_NAME=My App
      - DEBUG=true
    depends_on: # 依存関係
      - database
    networks: # ネットワーク
      - app-network
    volumes: # ボリュームマウント
      - ./data:/app/data

  database: # データベースサービス
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app-network

networks: # ネットワーク定義
  app-network:
    driver: bridge

volumes: # ボリューム定義
  db_data:
```

## 🔍 主要コンポーネントの詳細

### 1. services セクション

#### A. ビルド設定

```yaml
services:
  app:
    build: .                    # 現在ディレクトリのDockerfileを使用
    # または
    build:
      context: .
      dockerfile: Dockerfile.dev
```

#### B. 環境変数設定

```yaml
services:
  app:
    environment:
      # リスト形式
      - APP_NAME=My Application
      - DEBUG=true
      - DB_HOST=database

    # または辞書形式
    environment:
      APP_NAME: My Application
      DEBUG: true
      DB_HOST: database
```

#### C. 環境変数ファイル使用

```yaml
services:
  app:
    env_file:
      - .env.development
      - .env.local
```

#### D. 依存関係設定

```yaml
services:
  app:
    depends_on:
      - database # データベースが起動してからアプリを起動
      - redis # Redisが起動してからアプリを起動
```

### 2. networks セクション

```yaml
networks:
  app-network:
    driver: bridge # デフォルト

  # カスタムネットワーク
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### 3. volumes セクション

```yaml
volumes:
  # 名前付きボリューム（データ永続化）
  postgres_data:
  redis_data:

  # 外部ボリューム
  external_data:
    external: true
```

## 🚀 基本的なコマンド

### 起動・停止コマンド

```bash
# 全サービス起動（フォアグラウンド）
docker-compose up

# 全サービス起動（バックグラウンド）
docker-compose up -d

# 特定サービスのみ起動
docker-compose up app-dev
docker-compose up database redis

# サービス停止
docker-compose stop

# サービス停止＋削除（ボリュームは保持）
docker-compose down

# ボリュームも削除
docker-compose down -v

# イメージも削除
docker-compose down --rmi all
```

### 管理コマンド

```bash
# ログ確認
docker-compose logs
docker-compose logs app-dev
docker-compose logs -f app-dev  # リアルタイム表示

# サービス一覧
docker-compose ps

# 実行中のコンテナでコマンド実行
docker-compose exec app-dev bash
docker-compose exec database psql -U user -d myapp

# 新しいコンテナでコマンド実行
docker-compose run app-dev python manage.py migrate

# 設定確認
docker-compose config
```

### ビルド関連

```bash
# イメージビルド
docker-compose build

# 強制リビルド
docker-compose build --no-cache

# ビルド後に起動
docker-compose up --build
```

## 🔍 実用的なパターン

### 1. 開発・本番環境の使い分け

```yaml
services:
  # 開発環境
  app-dev:
    build: .
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
      - DB_HOST=postgres-dev
    depends_on:
      - postgres-dev
      - redis-dev

  # 本番環境
  app-prod:
    build: .
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - DB_HOST=postgres-prod
    depends_on:
      - postgres-prod
      - redis-prod
```

### 2. サービス間通信

```yaml
services:
  web:
    environment:
      # ❌ localhost は使えない
      - DATABASE_URL=postgres://user:pass@localhost:5432/db

      # ✅ サービス名を使用
      - DATABASE_URL=postgres://user:pass@database:5432/db
      - REDIS_URL=redis://cache:6379/0

  database: # ← このサービス名で通信
    image: postgres:15

  cache: # ← このサービス名で通信
    image: redis:7
```

### 3. データ永続化

```yaml
services:
  database:
    image: postgres:15
    volumes:
      # 名前付きボリューム（推奨）
      - postgres_data:/var/lib/postgresql/data

      # ホストディレクトリマウント（開発用）
      - ./data:/var/lib/postgresql/data

      # 設定ファイル
      - ./postgres.conf:/etc/postgresql/postgresql.conf:ro

volumes:
  postgres_data: # Docker管理の永続ボリューム
```

### 4. ポート公開

```yaml
services:
  web:
    ports:
      - "8000:8000" # ホスト:コンテナ
      - "127.0.0.1:8000:8000" # 特定IPのみ

  database:
    ports:
      - "5432:5432" # 開発時のみ（本番では非推奨）
    # 本番では expose のみ使用
    expose:
      - "5432" # コンテナ間通信のみ
```

## 🔍 環境別設定ファイル

### 複数ファイルの使い分け

```bash
# 基本設定 + 開発環境
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# 基本設定 + 本番環境
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

#### docker-compose.yml（共通設定）

```yaml
version: "3.8"
services:
  app:
    build: .
  database:
    image: postgres:15
```

#### docker-compose.dev.yml（開発環境）

```yaml
version: "3.8"
services:
  app:
    environment:
      - DEBUG=true
    volumes:
      - .:/app # ソースコードのホットリロード
    ports:
      - "8000:8000"
```

#### docker-compose.prod.yml（本番環境）

```yaml
version: "3.8"
services:
  app:
    environment:
      - DEBUG=false
    restart: unless-stopped
```

## 🎯 ベストプラクティス

### 1. セキュリティ

```yaml
services:
  app:
    # ❌ パスワードを直接記述しない
    environment:
      - DB_PASSWORD=secret123

    # ✅ 環境変数ファイルを使用
    env_file:
      - .env.local # .gitignoreに追加
```

### 2. 再起動ポリシー

```yaml
services:
  app:
    restart: unless-stopped # 本番環境推奨
    # restart: always        # 常に再起動
    # restart: on-failure    # 失敗時のみ再起動
    # restart: "no"          # 再起動しない（デフォルト）
```

### 3. ヘルスチェック

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 4. リソース制限

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
```

## 🚨 よくある問題と解決法

### 1. サービス間通信ができない

```yaml
# ❌ 問題：同じネットワークにない
services:
  app:
    networks: [frontend]
  database:
    networks: [backend]  # 異なるネットワーク

# ✅ 解決：同じネットワークに配置
services:
  app:
    networks: [app-network]
  database:
    networks: [app-network]
```

### 2. ポートが競合する

```bash
# エラー: Port 5432 is already in use
# 解決：別のポートを使用
services:
  database:
    ports:
      - "5433:5432"  # ホスト側のポートを変更
```

### 3. ボリュームの権限問題

```yaml
services:
  app:
    user: "1000:1000" # ユーザーID指定
    volumes:
      - ./data:/app/data
```

## 📋 チェックリスト

### 開発環境設定

- [ ] ソースコードのホットリロード設定
- [ ] ログレベルを DEBUG に設定
- [ ] 開発用データベース・キャッシュの設定
- [ ] ポート公開設定

### 本番環境設定

- [ ] 機密情報の外部化（env_file 使用）
- [ ] 再起動ポリシーの設定
- [ ] ヘルスチェックの設定
- [ ] リソース制限の設定
- [ ] 不要なポート公開の削除

### セキュリティ

- [ ] パスワードをコードに埋め込まない
- [ ] .env ファイルを .gitignore に追加
- [ ] 本番環境でのデバッグ無効化
- [ ] 不要なサービスの削除

## 🎯 Docker Compose vs Kubernetes

| 用途                   | Docker Compose      | Kubernetes      |
| ---------------------- | ------------------- | --------------- |
| **ローカル開発**       | ✅ 最適             | ❌ 複雑すぎる   |
| **小規模本番**         | ✅ 適している       | ❌ オーバーキル |
| **大規模本番**         | ❌ 限界がある       | ✅ 最適         |
| **マルチサーバー**     | ❌ 単一サーバーのみ | ✅ 対応         |
| **オートスケーリング** | ❌ 手動             | ✅ 自動         |

Docker Compose は**開発環境**と**小〜中規模の本番環境**で非常に有効です！

## 🔧 Docker Compose での .env ファイル読み込み

Docker Compose では `docker run --env-file` とは異なる方法で環境変数ファイルを読み込みます。

### 1. 自動読み込み（`.env` ファイル）

Docker Compose は **自動的に `.env` ファイルを読み込みます**：

```bash
# ファイル構造
.
├── docker-compose.yml
└── .env                 # ← 自動で読み込まれる
```

#### .env ファイルの例：

```bash
# .env
APP_NAME=Auto Loaded App
ENVIRONMENT=development
DEBUG=true
DB_HOST=postgres-dev
DB_PASSWORD=secret123
```

#### docker-compose.yml での使用：

```yaml
services:
  app:
    environment:
      - APP_NAME=${APP_NAME} # .envから読み込み
      - ENVIRONMENT=${ENVIRONMENT}
      - DEBUG=${DEBUG}
      - DB_HOST=${DB_HOST}
      - DB_PASSWORD=${DB_PASSWORD}
```

### 2. 明示的指定（`env_file`）

特定の .env ファイルを明示的に指定：

```yaml
services:
  app-dev:
    env_file:
      - .env.development # ← 明示的に指定
    environment:
      - ADDITIONAL_VAR=value

  app-prod:
    env_file:
      - .env.production # ← 本番用設定
```

### 3. 複数ファイルの組み合わせ

```yaml
services:
  app:
    env_file:
      - .env # 共通設定
      - .env.local # ローカル設定（.gitignoreに追加）
      - .env.development # 環境固有設定
    environment:
      - OVERRIDE_VAR=value # 最優先で設定される
```

### 4. 優先順位

```
1. environment セクション（最優先）
2. env_file で指定したファイル
3. .env ファイル（自動読み込み）
4. Dockerfile の ENV（最低優先）
```

### 5. docker run との比較

|                  | docker run             | docker-compose             |
| ---------------- | ---------------------- | -------------------------- |
| **自動読み込み** | ❌ なし                | ✅ `.env`ファイル          |
| **ファイル指定** | `--env-file .env.prod` | `env_file: [.env.prod]`    |
| **個別指定**     | `-e VAR=value`         | `environment: [VAR=value]` |
| **複数ファイル** | ❌ 1 ファイルのみ      | ✅ 複数ファイル対応        |
| **変数展開**     | ❌ なし                | ✅ `${VARIABLE}` 記法      |

### 6. 実用的なパターン

#### 開発環境での設定例：

```yaml
services:
  app-dev:
    env_file:
      - .env # 共通設定
      - .env.development # 開発固有設定
    environment:
      - APP_NAME=Dev Override App # 最優先
      - DEBUG=true
```

#### 本番環境での設定例：

```yaml
services:
  app-prod:
    env_file:
      - .env # 共通設定
      - .env.production # 本番固有設定
    environment:
      - API_KEY=${API_KEY} # 外部から注入される値
```

### 7. セキュリティのベストプラクティス

```bash
# .gitignore に追加すべきファイル
.env.local
.env.production
.env.*.local

# コミットしても良いファイル
.env.example
.env.development  # 機密情報を含まない場合のみ
```

Docker Compose では **宣言的** に環境変数を管理でき、複数環境の設定が非常に簡単になります！
