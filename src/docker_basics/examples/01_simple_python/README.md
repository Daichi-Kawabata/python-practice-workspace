# シンプルな Python Docker アプリ

## 概要

最もシンプルな Python アプリケーションの Docker コンテナ化例です。
外部依存関係がなく、Docker の基本概念を学習するのに適しています。

## ファイル構成

```
01_simple_python/
├── Dockerfile      # Dockerイメージ作成用の設定ファイル
├── app.py          # Python アプリケーション
├── .dockerignore   # Dockerイメージに含めないファイル指定
└── README.md       # このファイル
```

## 実行手順

### 1. Docker イメージの構築

```bash
# このディレクトリで実行
docker build -t simple-python-app .
```

### 2. コンテナの実行

```bash
# 基本実行
docker run simple-python-app

# 環境変数を追加して実行
docker run -e APP_ENV=production -e DOCKER_EXAMPLE=true simple-python-app

# インタラクティブモードで実行
docker run -it simple-python-app sh
```

### 3. イメージとコンテナの管理

```bash
# 作成されたイメージを確認
docker images

# 実行中のコンテナを確認
docker ps

# 全てのコンテナを確認（停止中も含む）
docker ps -a

# 不要なコンテナを削除
docker container prune

# 不要なイメージを削除
docker image prune
```

## Dockerfile の解説

```dockerfile
# ベースイメージの指定
FROM python:3.11-alpine
```

- `python:3.11-alpine`: 軽量な Alpine Linux ベースの Python 3.11 イメージ
- Alpine Linux は小さなサイズが特徴（通常の Linux イメージより 80%以上小さい）

```dockerfile
# 作業ディレクトリの設定
WORKDIR /app
```

- コンテナ内での作業ディレクトリを `/app` に設定
- 以降のコマンドはこのディレクトリで実行される

```dockerfile
# ファイルのコピー
COPY app.py .
```

- ホスト側の `app.py` をコンテナの `/app/app.py` にコピー
- `.` は現在の作業ディレクトリ（`/app`）を指す

```dockerfile
# 環境変数の設定
ENV APP_ENV=docker
ENV PYTHONUNBUFFERED=1
```

- `APP_ENV`: アプリケーション独自の環境変数
- `PYTHONUNBUFFERED=1`: Python の出力をバッファリングしない（ログの即座表示）

```dockerfile
# 非rootユーザーの作成と切り替え
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

- セキュリティ向上のため、root ユーザーではなく専用ユーザーで実行
- コンテナのセキュリティベストプラクティス

```dockerfile
# 実行コマンドの指定
CMD ["python", "app.py"]
```

- コンテナ起動時に実行されるデフォルトコマンド
- JSON 配列形式で指定（推奨）

## .dockerignore の活用

`.dockerignore`ファイルは、Docker イメージに含めたくないファイルやディレクトリを指定します：

- **Git 関連**: `.git`, `.gitignore`
- **Python 関連**: `__pycache__`, `*.pyc`, `.venv`
- **IDE 関連**: `.vscode`, `.idea`
- **OS 関連**: `.DS_Store`, `Thumbs.db`

これにより：

- イメージサイズの削減
- ビルド時間の短縮
- セキュリティの向上（機密ファイルの除外）

## 学習ポイント

1. **イメージサイズの比較**

   ```bash
   # 標準イメージサイズを確認
   docker build -t simple-python-standard -f Dockerfile.standard .
   docker images | grep simple-python
   ```

2. **環境変数の活用**

   - アプリケーションの設定をコンテナ実行時に変更可能
   - 開発・ステージング・本番環境での設定切り替えが容易

3. **セキュリティ考慮**
   - 非 root ユーザーでの実行
   - 不要なファイルの除外

## 次のステップ

- 依存関係があるアプリケーション（`02_requirements/`）
- 環境変数を活用したアプリケーション（`03_environment/`）
- Web アプリケーションのコンテナ化（`fastapi_example/`）
