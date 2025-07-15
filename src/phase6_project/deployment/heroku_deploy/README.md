
# FastAPI Todo APIをHerokuにデプロイする手順

このドキュメントでは、`src/phase4_web_frameworks/exercises/todo_api`で作成したFastAPIアプリケーションをHerokuにデプロイする方法を解説します。

## 0. 前提条件

- [Herokuアカウント](https://signup.heroku.com/)が作成済みであること。
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)がインストール済みであること。
- [Git](https://git-scm.com/downloads)がインストール済みであること。
- `todo_api`のディレクトリで作業していることを想定しています。

## 1. デプロイ準備

まず、Herokuにデプロイするために、プロジェクトの構成をいくつか変更・追加する必要があります。

### 1.1. `requirements.txt`の更新

HerokuのPostgreSQLデータベースに接続するための`psycopg2-binary`と、本番環境用のWebサーバー`gunicorn`を追加します。

**`requirements.txt`に以下の2行を追記してください:**

```txt
gunicorn
psycopg2-binary
```

### 1.2. `Procfile`の作成

Herokuは`Procfile`というファイルを見て、アプリケーションをどのように起動するかを判断します。
プロジェクトのルートディレクトリ（`todo_api`直下）に`Procfile`という名前のファイルを作成し、以下の内容を記述してください。

**`Procfile`:**
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
release: alembic upgrade head
```

- `web`: Webプロセスを起動するコマンドです。`gunicorn`を使って`app.main`モジュールの`app`インスタンスを起動します。
- `release`: デプロイが完了する前に一度だけ実行されるコマンドです。ここでは`alembic`を使ってデータベースのマイグレーションを自動で実行するように設定しています。

### 1.3. データベース設定の変更 (`app/database.py`)

Herokuでは、データベースの接続情報が`DATABASE_URL`という環境変数で提供されます。
ローカルのSQLite設定と、HerokuのPostgreSQL設定を両方扱えるように`app/database.py`を修正します。

**`app/database.py`を以下のように書き換えてください:**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# HerokuのDATABASE_URLを優先的に使用し、なければローカルのSQLiteを使用
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# PostgreSQLの場合、URLのプレフィックスを修正
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLiteの場合のみ必要
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### 1.4. Alembic設定の変更 (`app/alembic.ini`)

AlembicがHerokuのデータベースを参照できるように、`alembic.ini`を修正します。

**`app/alembic.ini`の`sqlalchemy.url`の行を以下のようにコメントアウトし、環境変数から読み込むようにします。**

```ini
# ... (前略) ...

# the output encoding used when dealing with script files.
# output_encoding = utf-8

# sqlalchemy.url = sqlite:///./test.db  <- この行をコメントアウトするか削除
sqlalchemy.url = ${DATABASE_URL}       <- この行を追記

# ... (後略) ...
```
**修正箇所:** `[alembic]`セクションの`sqlalchemy.url`

**重要:** `alembic.ini`で環境変数を直接参照するために、`main`セクションの先頭に`config_args`を追加する必要があるかもしれません。
```ini
[alembic]
# ...
script_location = alembic
# ...
prepend_sys_path = .
# ...
sqlalchemy.url = %(here)s/../app.db # ここを修正
```
上記がうまくいかない場合は、`app/alembic/env.py`を直接編集する方法もあります。

**`app/alembic/env.py`の修正:**
`target_metadata`が定義されているあたりに、以下のコードを追加して、`alembic.ini`のURL設定を上書きします。

```python
# ... (前略) ...
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# ★★★ ここから追加 ★★★
# HerokuのDATABASE_URLを読み込む
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
# ★★★ ここまで追加 ★★★

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.models.user import Base as UserBase # 例
from app.models.task import Base as TaskBase # 例
target_metadata = [UserBase.metadata, TaskBase.metadata] # 実際のモデルに合わせて修正

# ... (後略) ...
```
*注意:* `target_metadata`の部分は、`todo_api`プロジェクトで定義されているモデルの`Base.metadata`をすべて含めるように修正してください。

## 2. Herokuへのデプロイ

準備が整ったら、いよいよHerokuにデプロイします。

### 2.1. Herokuにログイン

```bash
heroku login
```

### 2.2. Gitリポジトリの初期化

`todo_api`ディレクトリでGitリポジトリを初期化し、変更をコミットします。

```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 2.3. Herokuアプリの作成

```bash
heroku create your-app-name  # 'your-app-name'は好きな名前に変更
```
名前を省略するとランダムな名前が生成されます。

### 2.4. Heroku Postgresアドオンの追加

```bash
heroku addons:create heroku-postgresql:hobby-dev
```
これにより、データベースが作成され、`DATABASE_URL`環境変数が自動で設定されます。

### 2.5. 環境変数の設定

JWTトークンの生成に必要な`SECRET_KEY`と`ALGORITHM`をHerokuに設定します。
（`app/core/config.py`などで定義されている値を設定してください）

```bash
heroku config:set SECRET_KEY='your_secret_key'
heroku config:set ALGORITHM='your_algorithm'
# 例: heroku config:set SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
# 例: heroku config:set ALGORITHM='HS256'
```

### 2.6. デプロイ

Gitを使ってHerokuにコードをプッシュします。これがデプロイのトリガーとなります。

```bash
git push heroku main  # もしくは master
```

プッシュが完了すると、Heroku上でビルドが開始され、`release`フェーズで定義した`alembic upgrade head`が実行されてデータベースのマイグレーションが行われます。

## 3. 動作確認

### 3.1. アプリケーションを開く

```bash
heroku open
```
ブラウザでデプロイしたアプリケーションのURLが開きます。`/docs`にアクセスして、APIドキュメントが表示されれば成功です。

### 3.2. ログの確認

もし問題が発生した場合は、以下のコマンドでログを確認できます。

```bash
heroku logs --tail
```

以上で、FastAPIアプリケーションのHerokuへのデプロイは完了です。
