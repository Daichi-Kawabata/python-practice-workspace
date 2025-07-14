# FastAPI Docker Application
FROM python:3.11-alpine

# メタデータ
LABEL maintainer="your-email@example.com"
LABEL description="FastAPI Application with Docker"

# 作業ディレクトリを設定
WORKDIR /app

# Alpineで必要なビルドツールをインストール
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# 依存関係ファイルを先にコピー（Docker層キャッシュの最適化）
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY app.py .

# 環境変数を設定
ENV APP_NAME="FastAPI Docker App"
ENV APP_VERSION="1.0.0"
ENV DEBUG=false
ENV HOST=0.0.0.0
ENV PORT=8000
ENV LOG_LEVEL=info
ENV PYTHONUNBUFFERED=1
ENV CORS_ORIGINS="http://localhost:3000,http://localhost:8080"

# セキュリティ向上のため非rootユーザーを作成
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# ポートを公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# アプリケーションを実行
CMD ["python", "app.py"]
