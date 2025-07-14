# シンプルなPython DockerFileの例
# Python 3.11の軽量版を使用
FROM python:3.11-alpine

# 作業ディレクトリを設定
WORKDIR /app

# アプリケーションファイルをコピー
COPY app.py .

# 環境変数を設定（例）
ENV APP_ENV=docker
ENV PYTHONUNBUFFERED=1

# セキュリティ向上のため非rootユーザーを作成
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# アプリケーションを実行
CMD ["python", "app.py"]
