# FastAPI + Nginx Docker Compose 例

## 🎯 学習目標

この例では、**本格的な Web アプリケーション構成**を学びます：

### 1. 🌐 なぜ Nginx が必要？

#### 🔴 FastAPI 単体の問題点

```
[Client] → [FastAPI:8000]
```

- **セキュリティ**: 外部に直接公開はリスク
- **パフォーマンス**: 静的ファイル配信が苦手
- **SSL**: HTTPS 設定が複雑
- **負荷**: 高負荷時に不安定

#### 🟢 Nginx + FastAPI の構成

```
[Client] → [Nginx:80] → [FastAPI:8000]
```

- **リバースプロキシ**: 外部からの接続を安全に中継
- **静的ファイル配信**: CSS/JS/画像を高速配信
- **SSL 終端**: HTTPS 証明書を nginx で一元管理
- **負荷分散**: 複数の FastAPI インスタンスに分散可能
- **キャッシュ**: レスポンスをキャッシュして高速化

### 2. 🏗️ アーキテクチャパターン

#### マイクロサービス構成

```yaml
services:
  nginx: # Web Server / Reverse Proxy
    image: nginx:alpine
    ports: ["80:80"]

  fastapi-app: # API Server
    build: .
    expose: ["8000"] # 外部公開しない
```

#### ネットワーク分離

- **nginx**: 外部からアクセス可能 (port 80)
- **fastapi-app**: 内部通信のみ (expose 8000)
- **Docker Network**: コンテナ間の安全な通信

### 3. 🔧 設定のポイント

#### nginx.conf の要点

```nginx
upstream fastapi_backend {
    server fastapi-app:8000;  # サービス名で通信
}

location / {
    proxy_pass http://fastapi_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

#### docker-compose.yml の要点

```yaml
depends_on:
  - fastapi-app # 起動順序の制御

healthcheck: # ヘルスチェック
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

### 4. 🚀 実運用での利点

#### 本格的な Web アプリ構成

- **フロントエンド**: nginx で配信
- **API**: FastAPI で処理
- **データベース**: 別コンテナで分離
- **監視**: ヘルスチェック + ログ収集

#### スケールアウト対応

```yaml
fastapi-app:
  scale: 3 # 3インスタンス起動
```

nginx が自動的に負荷分散！

### 5. 🧪 テスト方法

```bash
# 1. 全体起動
docker-compose up --build

# 2. nginx経由でアクセス
curl http://localhost/

# 3. 直接FastAPIアクセス（内部のみ）
docker-compose exec fastapi-app curl http://localhost:8000/

# 4. ヘルスチェック確認
docker-compose ps
```

## 💡 ここが Docker の真価！

**従来の問題**:

- nginx 設定が複雑
- 複数サービスの依存関係管理が困難
- 開発環境と本番環境の差

**Docker で解決**:

- `docker-compose.yml` で全て定義
- ワンコマンドで完全な環境構築
- 開発 = 本番 の環境保証

これで **"本格的な Web アプリケーション"** の構成が理解できます！
