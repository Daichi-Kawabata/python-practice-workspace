# 依存関係を含むPython DockerFileの例
FROM python:3.11-alpine

# 作業ディレクトリを設定
WORKDIR /app

# Alpineで必要なビルドツールをインストール
# pandas/numpyのコンパイルに必要
RUN apk add --no-cache \
    gcc \
    g++ \
    gfortran \
    musl-dev \
    linux-headers \
    openblas-dev \
    lapack-dev \
    && rm -rf /var/cache/apk/*

# 依存関係ファイルを先にコピー（Docker層キャッシュの最適化）
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY app.py .

# 環境変数を設定
ENV APP_ENV=docker
ENV DEBUG=false
ENV PYTHONUNBUFFERED=1

# セキュリティ向上のため非rootユーザーを作成
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# アプリケーションを実行
CMD ["python", "app.py"]
