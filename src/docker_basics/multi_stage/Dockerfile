# マルチステージビルドを使用した最適化されたDockerfile
# 本番環境向けの軽量なイメージを作成

# ========================================
# ビルドステージ（依存関係のインストール）
# ========================================
FROM python:3.11-alpine as builder

# ビルドに必要なツールをインストール
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    git

# pipのアップグレードと仮想環境の作成
RUN pip install --upgrade pip && \
    python -m venv /opt/venv

# 仮想環境をアクティベート
ENV PATH="/opt/venv/bin:$PATH"

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール（仮想環境内）
RUN pip install --no-cache-dir -r requirements.txt

# ========================================
# 本番ステージ（実行環境）
# ========================================
FROM python:3.11-alpine

# メタデータ
LABEL maintainer="your-email@example.com"
LABEL description="Multi-stage FastAPI Application"
LABEL version="1.0.0"

# 作業ディレクトリを設定
WORKDIR /app

# ビルドステージから仮想環境をコピー
COPY --from=builder /opt/venv /opt/venv

# 仮想環境のPATHを設定
ENV PATH="/opt/venv/bin:$PATH"

# 実行時に必要な最小限のパッケージをインストール
RUN apk add --no-cache \
    ca-certificates \
    && rm -rf /var/cache/apk/*

# アプリケーションファイルをコピー
COPY app.py .

# 環境変数を設定
ENV APP_NAME="Multi-stage FastAPI App"
ENV APP_VERSION="1.0.0"
ENV DEBUG=false
ENV HOST=0.0.0.0
ENV PORT=8000
ENV LOG_LEVEL=info
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# セキュリティ向上のため非rootユーザーを作成
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app /opt/venv
USER appuser

# ポートを公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# アプリケーションを実行
CMD ["python", "app.py"]
