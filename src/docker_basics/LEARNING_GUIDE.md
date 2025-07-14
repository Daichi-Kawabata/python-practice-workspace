# Docker 実践学習ガイド

## 段階的学習アプローチ

このガイドでは、作成した Docker サンプルを使って段階的に Docker の概念と技術を学習します。

## 学習ステップ

### ステップ 1: Docker 基本操作の習得

#### 1.1 シンプルな Python アプリ (`01_simple_python/`)

```bash
# ディレクトリに移動
cd examples/01_simple_python

# イメージをビルド
docker build -t simple-python-app .

# イメージサイズを確認
docker images simple-python-app

# コンテナを実行
docker run simple-python-app

# 環境変数を設定して実行
docker run -e APP_ENV=production simple-python-app

# インタラクティブモードで実行
docker run -it simple-python-app sh
```

**学習ポイント:**

- Dockerfile の基本構造
- `FROM`, `WORKDIR`, `COPY`, `ENV`, `CMD`の役割
- `.dockerignore`の効果
- Alpine Linux の軽量性

#### 1.2 依存関係を含むアプリ (`02_requirements/`)

```bash
cd examples/02_requirements

# イメージをビルド（時間がかかる）
docker build -t requirements-python-app .

# サイズ比較
docker images | grep -E "(simple-python-app|requirements-python-app)"

# デバッグモードで実行
docker run -e DEBUG=true requirements-python-app

# 本番モードで実行
docker run -e APP_ENV=production -e DEBUG=false requirements-python-app
```

**学習ポイント:**

- `requirements.txt`の活用
- ビルドツール（gcc 等）の必要性
- レイヤーキャッシュの重要性
- 依存関係によるイメージサイズ増加

### ステップ 2: 環境変数管理の学習

#### 2.1 環境変数アプリ (`03_environment/`)

```bash
cd examples/03_environment

# 基本実行
docker build -t env-demo-app .
docker run env-demo-app

# 開発環境設定で実行
docker run --env-file .env.development env-demo-app

# 本番環境設定で実行
docker run --env-file .env.production env-demo-app

# 個別環境変数を設定
docker run -e ENVIRONMENT=staging \
           -e DEBUG=true \
           -e MAX_CONNECTIONS=15 \
           env-demo-app
```

**学習ポイント:**

- 環境変数による設定管理
- `--env-file`の使用方法
- 開発・本番環境の設定分離
- セキュリティを考慮した機密情報管理

#### 2.2 Docker Compose での環境管理

```bash
# 開発環境用サービス起動
docker-compose up app-dev postgres-dev redis-dev

# 本番環境用サービス起動
docker-compose up app-prod postgres-prod redis-prod

# バックグラウンド実行
docker-compose up -d app-dev postgres-dev redis-dev

# ログ確認
docker-compose logs app-dev

# サービス停止・削除
docker-compose down
```

**学習ポイント:**

- 複数コンテナの連携
- ネットワーク自動作成
- ボリュームによるデータ永続化
- サービス間の依存関係

### ステップ 3: Web アプリケーションのコンテナ化

#### 3.1 FastAPI アプリケーション (`fastapi_example/`)

```bash
cd fastapi_example

# イメージビルド
docker build -t fastapi-docker-app .

# アプリケーション起動
docker run -d -p 8000:8000 --name fastapi-container fastapi-docker-app

# ヘルスチェック
curl http://localhost:8000/health

# API ドキュメント確認
# ブラウザで http://localhost:8000/docs にアクセス

# ログ確認
docker logs fastapi-container

# コンテナ内部確認
docker exec -it fastapi-container sh

# コンテナ停止・削除
docker stop fastapi-container
docker rm fastapi-container
```

**学習ポイント:**

- ポートマッピング (`-p 8000:8000`)
- ヘルスチェックの実装
- ログ管理
- デーモンモード (`-d`) での実行

#### 3.2 Docker Compose での実行

```bash
# サービス起動
docker-compose up -d

# ヘルスチェック
curl http://localhost:8000/health

# Nginxを通したアクセス
curl http://localhost/health

# サービス状況確認
docker-compose ps

# ログ確認
docker-compose logs fastapi-app
docker-compose logs nginx

# サービス停止
docker-compose down
```

**学習ポイント:**

- リバースプロキシの設定
- サービス間通信
- ヘルスチェックの活用

### ステップ 4: 最適化技術の学習

#### 4.1 マルチステージビルド (`multi_stage/`)

```bash
cd multi_stage

# 通常のビルドとサイズ比較
docker build -f ../fastapi_example/Dockerfile -t fastapi-normal ../fastapi_example
docker build -t fastapi-multistage .

# サイズ比較
docker images | grep fastapi

# 実行
docker run -d -p 8001:8000 --name multistage-container fastapi-multistage

# テスト
curl http://localhost:8001/health
curl http://localhost:8001/metrics

# 停止
docker stop multistage-container
docker rm multistage-container
```

**学習ポイント:**

- マルチステージビルドによるサイズ最適化
- ビルド時と実行時の分離
- セキュリティ向上

## 実践的な演習課題

### 演習 1: 既存アプリケーションのコンテナ化

**課題:** これまで作成した FastAPI 設定管理アプリをコンテナ化してください。

```bash
# config_managementディレクトリから
cd ../../config_management/practical_examples/fastapi_config

# 演習用Dockerfileを作成
```

**要件:**

- マルチステージビルドを使用
- 環境変数で設定管理
- ヘルスチェック実装
- 非 root ユーザーで実行

### 演習 2: Docker Compose での統合

**課題:** データベース、Redis、FastAPI アプリケーションを統合したシステムを構築してください。

**要件:**

- PostgreSQL コンテナとの連携
- Redis コンテナでのキャッシュ
- 開発・本番環境の設定分離
- ボリュームでのデータ永続化

### 演習 3: CI/CD パイプライン準備

**課題:** GitHub Actions でのビルド・テスト・デプロイを想定した Dockerfile 作成

**要件:**

- テスト実行ステージの追加
- 本番イメージの最小化
- セキュリティスキャンの考慮

## デバッグとトラブルシューティング

### 一般的な問題と解決方法

#### 1. ビルドエラー

```bash
# ビルドプロセスの詳細確認
docker build --progress=plain --no-cache -t myapp .

# 特定ステップでの停止
docker build --target builder -t myapp-debug .
docker run -it myapp-debug sh
```

#### 2. 実行時エラー

```bash
# ログ確認
docker logs container-name

# コンテナ内部調査
docker exec -it container-name sh

# ポート使用状況確認
netstat -tulpn | grep 8000
```

#### 3. パフォーマンス問題

```bash
# リソース使用量確認
docker stats

# イメージレイヤー確認
docker history image-name

# 不要なコンテナ・イメージ削除
docker system prune -f
```

### ベストプラクティス チェックリスト

- [ ] 軽量なベースイメージの使用
- [ ] .dockerignore ファイルの作成
- [ ] 非 root ユーザーでの実行
- [ ] ヘルスチェックの実装
- [ ] 適切なログ設定
- [ ] 環境変数による設定管理
- [ ] マルチステージビルドの活用
- [ ] レイヤーキャッシュの最適化

## 次のステップ

1. **Kubernetes 学習**: コンテナオーケストレーション
2. **CI/CD 統合**: GitHub Actions, Jenkins 等
3. **モニタリング**: Prometheus, Grafana 等
4. **セキュリティ**: コンテナスキャン、シークレット管理
5. **本番デプロイ**: AWS ECS, Google Cloud Run 等
