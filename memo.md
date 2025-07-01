# 環境構築周辺

## venvアクティブ
```bash
.\.venv\Scripts\activate
```

## venv非アクティブ
```bash
deactivate
```

## Git管理について
- `.venv`フォルダは`.gitignore`に追加してGit管理から除外する
- 代わりに`requirements.txt`で依存関係を管理する

### requirements.txtの作成
```bash
pip freeze > requirements.txt
```

### 他の環境での環境再構築
```bash
pip install -r requirements.txt
```