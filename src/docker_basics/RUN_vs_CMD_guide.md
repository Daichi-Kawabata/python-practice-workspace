# RUN vs CMD の違い - 完全ガイド

## 🔍 基本的な違い

| コマンド | 実行タイミング                 | 目的                 |
| -------- | ------------------------------ | -------------------- |
| **RUN**  | **ビルド時**（`docker build`） | 環境構築・準備作業   |
| **CMD**  | **起動時**（`docker run`）     | アプリケーション実行 |

## 📅 実行タイミングの詳細

### RUN - ビルド時に実行

```dockerfile
FROM python:3.11-alpine
WORKDIR /app

# ⏰ これらは全て docker build の時に実行される
RUN echo "これはビルド時に実行されます"
RUN apk add --no-cache gcc
RUN pip install pandas
RUN mkdir /app/logs
RUN adduser appuser
```

**特徴：**

- イメージに結果が焼き込まれる
- 一度実行されると、次回ビルド時はキャッシュが使われる
- 毎回のコンテナ起動では実行されない

### CMD - 起動時に実行

```dockerfile
# ⏰ これは docker run の時に実行される
CMD ["python", "app.py"]
```

**特徴：**

- 毎回のコンテナ起動時に実行
- Dockerfile で 1 つだけ有効（最後の CMD が使われる）
- `docker run` 時に上書き可能

## ❌ よくある間違い

### 問題のある Dockerfile

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY app.py .
RUN python app.py  # ❌ これは間違い！
```

**何が起こるか：**

1. `docker build` 時に app.py が実行される
2. `docker run` 時には何も実行されない
3. アプリケーションが期待通りに動かない

### 正しい Dockerfile

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]  # ✅ これが正解！
```

## 🔍 適切な使い分け

### RUN を使う場面

```dockerfile
# ✅ 環境構築・準備作業
RUN pip install pandas              # ライブラリインストール
RUN mkdir -p /app/logs             # ディレクトリ作成
RUN chmod +x /app/script.sh        # 実行権限付与
RUN adduser --disabled-password appuser  # ユーザー作成
RUN apt-get update && apt-get install -y curl  # システムパッケージ
```

### CMD を使う場面

```dockerfile
# ✅ アプリケーション実行
CMD ["python", "app.py"]               # Pythonアプリ起動
CMD ["node", "server.js"]              # Node.jsアプリ起動
CMD ["nginx", "-g", "daemon off;"]     # Webサーバー起動
CMD ["python", "-m", "flask", "run"]   # Flaskアプリ起動
```

## 💡 実用的なテクニック

### 1. CMD の上書き

```bash
# Dockerfileで CMD ["python", "app.py"] と定義済み

# 通常の起動
$ docker run my-app
# → python app.py が実行される

# デバッグ用に別のスクリプトを実行
$ docker run my-app python debug.py
# → python debug.py が実行される（CMDが上書きされる）

# シェルに入る
$ docker run -it my-app bash
# → bashが実行される
```

### 2. 複数の CMD は最後だけ有効

```dockerfile
CMD ["echo", "first"]
CMD ["echo", "second"]    # ← これだけが実行される
CMD ["python", "app.py"]  # ← 実際に実行されるのはこれ
```

### 3. ENTRYPOINT との組み合わせ

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
# 結果: python app.py が実行される

# docker run時の動作
$ docker run my-app          # → python app.py
$ docker run my-app debug.py # → python debug.py
```

## 🎯 覚え方

| コマンド | 覚え方                             |
| -------- | ---------------------------------- |
| **RUN**  | **ランニング中**（ビルド中）に実行 |
| **CMD**  | **コマンド**をコンテナ起動時に実行 |

または

| コマンド | イメージ                                     |
| -------- | -------------------------------------------- |
| **RUN**  | **料理の下準備**（材料を切る、調味料を準備） |
| **CMD**  | **料理を食卓に出す**（実際に食べる）         |

## 🔍 実際の開発での例

### Web アプリケーションの場合

```dockerfile
FROM python:3.11-alpine

# RUN: 環境構築
RUN apk add --no-cache gcc musl-dev
RUN pip install flask gunicorn

# RUN: アプリケーションファイルの配置
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

# RUN: セキュリティ設定
RUN adduser --disabled-password appuser
USER appuser

# CMD: アプリケーション起動
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### データ処理バッチの場合

```dockerfile
FROM python:3.11-alpine

# RUN: 環境構築
RUN pip install pandas numpy

# RUN: スクリプト配置
COPY process_data.py .
COPY config.json .

# CMD: バッチ処理実行
CMD ["python", "process_data.py"]
```

## 📝 チェックリスト

- [ ] RUN は環境構築・準備作業に使う
- [ ] CMD はアプリケーション実行に使う
- [ ] RUN python app.py は避ける
- [ ] CMD は起動時に実行されることを理解している
- [ ] CMD は上書き可能であることを理解している
