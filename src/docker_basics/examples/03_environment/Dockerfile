# ここではdocker run時に--env-fileオプションを使用して設定することができます。
# ocker run --rm --env-file .env.production env-demo-app

# 環境変数を使用したアプリケーション用のDockerfile
FROM python:3.11-alpine

# メタデータ
LABEL maintainer="your-email@example.com"
LABEL description="Environment Variable Demo Application"

# 作業ディレクトリを設定
WORKDIR /app

# アプリケーションファイルをコピー
COPY app.py .

# 環境変数のデフォルト値を設定
ENV APP_NAME="Environment Demo App"
ENV APP_VERSION="1.0.0"
ENV ENVIRONMENT=development
ENV LOG_LEVEL=INFO

# データベース設定のデフォルト値
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=myapp
ENV DB_USER=user
ENV DB_PASSWORD=password

# Redis設定
ENV REDIS_URL=redis://localhost:6379/0

# API設定（本番では外部から注入）
ENV EXTERNAL_API_URL=https://api.example.com

# 機能フラグのデフォルト値
ENV DEBUG=false
ENV ENABLE_CACHE=true
ENV ENABLE_METRICS=false

# ネットワーク設定
ENV MAX_CONNECTIONS=10
ENV TIMEOUT_SECONDS=30.0
ENV ALLOWED_HOSTS=localhost,127.0.0.1

# JSON形式の設定例
ENV FEATURE_FLAGS="{\"new_ui\": true, \"beta_features\": false}"

# Python固有の環境変数
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# セキュリティ向上のため非rootユーザーを作成
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# アプリケーションを実行
CMD ["python", "app.py"]
