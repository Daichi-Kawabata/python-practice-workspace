# フェーズ 3: SQLAlchemy/ORM 演習課題

このディレクトリには、フェーズ 3 の演習課題が含まれています。

## 演習課題一覧

### 課題 1: CRUD 操作の実装

**ファイル**: `crud_operations.py`
**難易度**: ★★☆

基本的な CRUD 操作（Create, Read, Update, Delete）を実装します。

**実装すべき機能**:

- [ ] UserCRUD クラスの完成

  - [ ] create_user() - ユーザー作成
  - [ ] get_user_by_id() - ID 検索
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

### 課題 2: ブログ CLI アプリの実装

**ファイル**: `blog_cli.py`
**難易度**: ★★★

インタラクティブなブログ管理 CLI アプリケーションを実装します。

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

### 課題 3: Alembic マイグレーション

**難易度**: ★☆☆

Alembic を使用してデータベーススキーマの変更管理を学習します。

**実装すべき機能**:

- [x] Alembic の初期化
- [x] 初期マイグレーションファイルの作成
- [x] スキーマ変更の実践
  - [x] テーブル追加 (Comment テーブル)
  - [x] カラム追加 (User プロフィール関連カラム)
  - [x] インデックス変更 (パフォーマンス向上用インデックス)
- [x] マイグレーションの実行とロールバック

**実習ファイル**:

- `alembic_migration_practice.py` - 実習用プログラム
- `migration_models.py` - 実習用モデル定義
- `ALEMBIC_MIGRATION_GUIDE.md` - 詳細な実習ガイド

**完了した実習**:

- ✅ 実習 1: Comment テーブルの追加
- ✅ 実習 2: User テーブルへのカラム追加
- ✅ 実習 3: パフォーマンス向上のためのインデックス作成
- ✅ 実習 4: マイグレーションのロールバック体験

## 学習の進め方

### Step 1: 基本理解

1. `../database.py` と `../models.py` を理解する
2. SQLAlchemy の基本概念を復習する

### Step 2: CRUD 操作の実装

1. `crud_operations.py` の骨格を確認
2. 一つずつメソッドを実装
3. テストしながら動作確認

### Step 3: CLI アプリの実装

1. `blog_cli.py` の基本構造を理解
2. メニューシステムから実装開始
3. 段階的に機能を追加

### Step 4: マイグレーション学習

1. Alembic のドキュメントを参照
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
