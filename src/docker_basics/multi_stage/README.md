# 🏗️ マルチステージビルド（Multi-Stage Build）

## 🎯 学習目標

この例では、**Docker の最重要テクニック**の一つである**マルチステージビルド**を学びます：

### 📚 なぜマルチステージビルドが重要？

#### 🔴 従来の問題（シングルステージ）

```dockerfile
FROM python:3.11-alpine
RUN apk add gcc musl-dev linux-headers git  # ビルドツール
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

**問題点:**

- ✗ ビルドツール（gcc, git 等）が本番イメージに残る
- ✗ イメージサイズが巨大（500MB〜1GB+）
- ✗ セキュリティリスク（不要なツールが攻撃対象）
- ✗ 起動が遅い（大きなイメージのダウンロード）

#### 🟢 マルチステージの解決策

```dockerfile
# ステージ1: ビルド専用
FROM python:3.11-alpine as builder
RUN apk add gcc musl-dev  # ビルドツールをインストール
RUN pip install -r requirements.txt  # 依存関係をビルド

# ステージ2: 実行専用
FROM python:3.11-alpine
COPY --from=builder /opt/venv /opt/venv  # 必要な部分だけコピー
COPY app.py .
CMD ["python", "app.py"]
```

**利点:**

- ✅ 最終イメージは最小限（50-100MB）
- ✅ セキュリティ向上（ビルドツールなし）
- ✅ デプロイ高速化
- ✅ ストレージ効率化

## 🔍 この Dockerfile の詳細解説

### 1. 🏗️ ビルドステージ（builder）

```dockerfile
FROM python:3.11-alpine as builder
```

- **目的**: 依存関係のコンパイルとインストール
- **特徴**: 重いビルドツールを含む
- **成果物**: 仮想環境（/opt/venv）

### 2. 🚀 本番ステージ（production）

```dockerfile
FROM python:3.11-alpine
COPY --from=builder /opt/venv /opt/venv
```

- **目的**: 実際の実行環境
- **特徴**: 最小限のパッケージのみ
- **成果物**: 軽量な本番イメージ

## 💡 重要なテクニック

### 1. 🔄 仮想環境の活用

```dockerfile
# ビルドステージ
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 本番ステージ
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```

### 2. 🔒 セキュリティ強化

```dockerfile
# 非rootユーザーで実行
RUN adduser --disabled-password appuser
USER appuser

# 環境変数でセキュリティ向上
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

### 3. 📊 ヘルスチェック

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

## 🧪 実践演習

### 1. イメージサイズの比較

```bash
# マルチステージビルド
docker build -t fastapi-multi .

# シングルステージ版を作って比較
docker images | grep fastapi
```

### 2. レイヤー構造の確認

```bash
# イメージの詳細情報
docker history fastapi-multi

# レイヤー分析
docker inspect fastapi-multi
```

### 3. セキュリティ検証

```bash
# コンテナ内のツール確認
docker run -it fastapi-multi sh
# gcc がインストールされていないことを確認
which gcc  # should return: not found
```

## 🚀 実運用での効果

### Before（シングルステージ）

- **イメージサイズ**: 800MB
- **プルタイム**: 5 分
- **セキュリティ**: ⚠️ ビルドツール含む

### After（マルチステージ）

- **イメージサイズ**: 120MB
- **プルタイム**: 30 秒
- **セキュリティ**: ✅ 最小限パッケージ

## 📋 学習チェックリスト

- [ ] マルチステージビルドの概念理解
- [ ] `FROM ... as builder` 構文の理解
- [ ] `COPY --from=builder` の使用方法
- [ ] イメージサイズの最適化効果確認
- [ ] セキュリティ向上の理解
- [ ] 仮想環境の活用方法
- [ ] ヘルスチェック設定
- [ ] 非 root ユーザー実行

## 🎯 次のステップ

1. **基本テスト**: この Dockerfile をビルド・実行
2. **比較実験**: シングルステージ版を作成して比較
3. **カスタマイズ**: 他の Python ライブラリで試す
4. **本格活用**: 実際のプロジェクトに適用

マルチステージビルドは、**Docker を本格的に使う上で必須の技術**です！ 🚀
