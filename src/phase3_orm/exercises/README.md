# フェーズ3: SQLAlchemy/ORM 演習課題

このディレクトリには、フェーズ3の演習課題が含まれています。

## 演習課題一覧

### 課題1: CRUD操作の実装
**ファイル**: `crud_operations.py`
**難易度**: ★★☆

基本的なCRUD操作（Create, Read, Update, Delete）を実装します。

**実装すべき機能**:
- [ ] UserCRUD クラスの完成
  - [ ] create_user() - ユーザー作成
  - [ ] get_user_by_id() - ID検索
  - [ ] get_user_by_username() - ユーザー名検索
  - [ ] update_user() - ユーザー情報更新
  - [ ] delete_user() - ユーザー削除

- [ ] CategoryCRUD クラスの完成
  - [ ] create_category() - カテゴリ作成
  - [ ] get_all_categories() - カテゴリ一覧
  - [ ] get_category_by_name() - 名前検索

- [ ] PostCRUD クラスの完成
  - [ ] create_post() - 記事作成
  - [ ] get_posts_by_author() - 著者別記事取得
  - [ ] search_posts() - 記事検索
  - [ ] update_post() - 記事更新
  - [ ] delete_post() - 記事削除

**参考実装**: `crud_operations_template.py` （完全実装版）

### 課題2: ブログCLIアプリの実装
**ファイル**: `blog_cli.py`
**難易度**: ★★★

インタラクティブなブログ管理CLIアプリケーションを実装します。

**実装すべき機能**:
- [ ] メインメニューシステム
- [ ] ユーザー管理機能
  - [ ] ユーザー作成
  - [ ] ユーザー一覧表示
  - [ ] ユーザー情報更新
- [ ] カテゴリ管理機能
  - [ ] カテゴリ作成
  - [ ] カテゴリ一覧表示
- [ ] 記事管理機能
  - [ ] 記事作成
  - [ ] 記事一覧表示
  - [ ] 記事検索
  - [ ] 記事公開/非公開切り替え
- [ ] 入力検証とエラーハンドリング

**参考実装**: `blog_cli_template.py` （完全実装版）

### 課題3: Alembicマイグレーション
**難易度**: ★☆☆

Alembicを使用してデータベーススキーマの変更管理を学習します。

**実装すべき機能**:
- [ ] Alembicの初期化
- [ ] 初期マイグレーションファイルの作成
- [ ] スキーマ変更の実践
  - [ ] テーブル追加
  - [ ] カラム追加/削除
  - [ ] インデックス変更
- [ ] マイグレーションの実行とロールバック

## 学習の進め方

### Step 1: 基本理解
1. `../database.py` と `../models.py` を理解する
2. SQLAlchemyの基本概念を復習する

### Step 2: CRUD操作の実装
1. `crud_operations.py` の骨格を確認
2. 一つずつメソッドを実装
3. テストしながら動作確認

### Step 3: CLIアプリの実装
1. `blog_cli.py` の基本構造を理解
2. メニューシステムから実装開始
3. 段階的に機能を追加

### Step 4: マイグレーション学習
1. Alembicのドキュメントを参照
2. 実際にスキーマ変更を体験
3. バージョン管理の概念を理解

## ヒントとコツ

### エラーハンドリング
```python
try:
    # データベース操作
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
    print(f"エラー: {e}")
```

### セッション管理
```python
with get_db_session() as session:
    # セッションを使った操作
    # with文を抜ける際に自動的にクローズ
```

### クエリの基本パターン
```python
# 単一取得
user = session.query(User).filter(User.id == user_id).first()

# 複数取得
users = session.query(User).filter(User.is_active == True).all()

# 条件検索
posts = session.query(Post).filter(
    Post.title.contains(keyword)
).order_by(Post.created_at.desc()).all()
```

頑張って実装してみてください！

詰まったときは、テンプレートファイルを参考にしてください。
