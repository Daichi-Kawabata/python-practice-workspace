# TODO アプリ起動方法

- カレントディレクトリは todo_api
- 以下コマンドどちらかを実行

```bash
# uvicornコマンドによる起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# pythonによるメインファイルの起動
python -m app.main
```
