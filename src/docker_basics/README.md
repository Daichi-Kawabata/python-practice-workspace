# Docker 基本学習

## 概要

このディレクトリでは、Python アプリケーションのコンテナ化について学習します。
Ruby/Rails、Golang の開発経験を活かし、Docker の基本概念から実践的な使用方法まで段階的に学習していきます。

## 学習目標

1. **Docker の基本概念を理解**

   - コンテナとイメージの違い
   - Dockerfile の書き方
   - Docker Compose の使用方法

2. **Python アプリケーションのコンテナ化**

   - 基本的な Python アプリケーションの Dockerfile 作成
   - FastAPI アプリケーションのコンテナ化
   - マルチステージビルドの活用

3. **実践的なコンテナ運用**
   - 環境変数の管理
   - ボリュームマウント
   - ネットワーク設定
   - 本番環境を想定した最適化

## ディレクトリ構成

```
docker_basics/
├── README.md                   # このファイル
├── examples/                   # 基本的なDockerの例
│   ├── 01_simple_python/      # シンプルなPythonアプリ
│   ├── 02_requirements/       # requirements.txtを使った例
│   └── 03_environment/        # 環境変数を使った例
├── fastapi_example/           # FastAPIアプリケーションの例
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── app/
│   └── requirements.txt
└── multi_stage/               # マルチステージビルドの例
    ├── Dockerfile
    └── app/
```

## 前提知識

- Python 基礎知識
- FastAPI/Flask 等の Web フレームワーク経験
- Git/GitHub 使用経験
- 他言語でのコンテナ使用経験（Ruby/Rails、Golang 等）

## Docker 基本概念

### イメージ（Image）

- アプリケーションとその依存関係を含む軽量で実行可能なパッケージ
- 読み取り専用のテンプレート
- Dockerfile から作成される

### コンテナ（Container）

- イメージの実行インスタンス
- 軽量で独立した実行環境
- 他のコンテナやホスト OS から分離されている

### Dockerfile

- Docker イメージを作成するための命令書
- テキストファイルで、イメージの構築手順を記述

### Docker Compose

- 複数のコンテナを定義・実行するためのツール
- YAML 形式でサービス、ネットワーク、ボリュームを定義

## 主要な Docker コマンド

```bash
# イメージの構築
docker build -t アプリ名 .

# コンテナの実行
docker run -p 8000:8000 アプリ名

# 実行中のコンテナ一覧
docker ps

# 全コンテナ一覧（停止中含む）
docker ps -a

# イメージ一覧
docker images

# コンテナの停止
docker stop コンテナID

# コンテナの削除
docker rm コンテナID

# イメージの削除
docker rmi イメージID

# Docker Composeでサービス起動
docker-compose up

# Docker Composeでサービス停止・削除
docker-compose down
```

## 学習の進め方

1. **基本例から開始** (`examples/`ディレクトリ)

   - シンプルな Python スクリプトのコンテナ化
   - 依存関係管理の理解
   - 環境変数の扱い方

2. **Web アプリケーションのコンテナ化** (`fastapi_example/`ディレクトリ)

   - FastAPI アプリケーションの Dockerfile 作成
   - Docker Compose を使ったサービス構成
   - データベースとの連携

3. **最適化技術の学習** (`multi_stage/`ディレクトリ)
   - マルチステージビルド
   - イメージサイズの最適化
   - セキュリティ考慮事項

## ベストプラクティス

### Dockerfile のベストプラクティス

1. **軽量なベースイメージを使用**

   ```dockerfile
   # 良い例：軽量なAlpineイメージ
   FROM python:3.11-alpine

   # 避ける例：フルサイズのイメージ
   FROM python:3.11
   ```

2. **レイヤーを最適化**

   ```dockerfile
   # 良い例：関連コマンドをまとめる
   RUN apt-get update && apt-get install -y \
       package1 \
       package2 \
       && rm -rf /var/lib/apt/lists/*

   # 避ける例：複数のRUN命令
   RUN apt-get update
   RUN apt-get install -y package1
   RUN apt-get install -y package2
   ```

3. **.dockerignore を活用**

   ```
   .git
   .gitignore
   .venv
   __pycache__
   *.pyc
   .pytest_cache
   .coverage
   ```

4. **非 root ユーザーで実行**
   ```dockerfile
   # セキュリティ向上のため非rootユーザーを作成
   RUN adduser --disabled-password --gecos '' appuser
   USER appuser
   ```

### 開発効率化の Tips

1. **開発用と本番用で Dockerfile を分ける**
2. **ボリュームマウントで開発効率向上**
3. **ヘルスチェックの実装**
4. **適切なログ出力設定**

## 参考リンク

- [Docker 公式ドキュメント](https://docs.docker.com/)
- [Docker Compose 公式ドキュメント](https://docs.docker.com/compose/)
- [Python Docker 公式イメージ](https://hub.docker.com/_/python)
- [Dockerfile ベストプラクティス](https://docs.docker.com/develop/dev-best-practices/)

## トラブルシューティング

### よくある問題と解決方法

1. **Windows でのパスの問題**

   - WSL2 の使用を推奨
   - パスの区切り文字に注意

2. **ポートが既に使用されている**

   ```bash
   # 使用中のポートを確認
   netstat -an | findstr :8000
   ```

3. **イメージサイズが大きい**

   - .dockerignore ファイルの確認
   - マルチステージビルドの検討
   - 軽量なベースイメージの使用

4. **コンテナ内でのファイル権限問題**
   - ユーザー ID の一致確認
   - 適切な権限設定
