# フェーズ3: ORMapper学習 (SQLAlchemy中心)

## 学習項目
- [x] SQLAlchemyの基本概念（モデル作成、CRUD操作）
- [x] データベース接続とセッション管理
- [x] リレーションの定義（1対多、多対多の実践）
- [x] クエリ構築、トランザクション管理
- [ ] DBマイグレーションツール（Alembic）利用法

## 演習課題
- [ ] ブログモデルの設計・CRUDのCLIアプリ作成
- [ ] RubyのActiveRecordやGolangのGORMとの比較メモを作成

## ファイル構成と学習内容

### `database.py` - データベース接続設定
- SQLAlchemyエンジンの作成と設定
- セッション管理（SessionLocal）
- Base クラス（モデルの親クラス）定義
- データベース初期化処理
- **学習ポイント**: エンジン、セッション、コネクションプールの概念

### `models.py` - SQLAlchemyモデル定義
- User, Category, Post, Tag モデルの定義
- リレーション（1対多、多対多）の実装
- 主キー、外部キー、インデックスの設定
- 型安全な`Mapped`と`mapped_column`の使用
- **学習ポイント**: ORMモデル、リレーション、データベース設計

### `crud_operations.py` - CRUD操作の実装（演習課題）
- **演習課題**: 基本的なCRUD操作を実装してください
- Create: ユーザー・記事・カテゴリの作成
- Read: ID検索、条件検索、リスト取得
- Update: モデルデータの更新
- Delete: レコード削除
- 複雑なクエリ（検索、フィルタリング、ソート）
- **学習ポイント**: データベース操作、クエリビルダー、エラーハンドリング
- **実装場所**: `exercises/crud_operations.py`
- **参考実装**: `exercises/crud_operations_template.py`

### `blog_cli.py` - ブログCLIアプリ（演習課題）
- **演習課題**: インタラクティブなCLIアプリを実装してください
- インタラクティブなメニューシステム
- ユーザー・カテゴリ・記事の管理機能
- 検索・一覧表示機能
- 入力検証とエラーハンドリング
- **学習ポイント**: 実践的なアプリケーション構築、CLI設計
- **実装場所**: `exercises/blog_cli.py`
- **参考実装**: `exercises/blog_cli_template.py`

### `orm_comparison.md` - ORM比較メモ
- SQLAlchemy vs ActiveRecord vs GORM の詳細比較
- モデル定義、CRUD操作、マイグレーション
- パフォーマンス、学習コスト、適用場面の比較
- **学習ポイント**: 技術選択の観点、各ORMの特徴理解

## 実行方法

### 1. 基本的なモデルテスト
```bash
cd src/phase3_orm
python -m database
python -m models
```

### 2. CRUD操作テスト
```bash
cd exercises
python -m crud_operations
```

### 3. ブログCLIアプリ実行
```bash
cd exercises
python -m blog_cli --interactive
```

**注意**: 演習課題として、これらのファイルは骨格のみ提供されています。実装は学習者が行ってください。

## 学習の進め方

### Step 1: 基本概念の理解
1. `database.py` を読んで SQLAlchemy の基本構造を理解
2. `models.py` でモデル定義とリレーションを学習
3. 実際にテストコードを実行してデータベースファイル作成を確認

### Step 2: CRUD操作の習得（演習課題）
1. `exercises/crud_operations.py` の骨格を確認
2. テンプレート (`exercises/crud_operations_template.py`) を参考に実装
3. 一つずつメソッドを実装し、テストしながら動作確認

### Step 3: 実践アプリケーション構築（演習課題）
1. `exercises/blog_cli.py` の基本構造を理解
2. テンプレート (`exercises/blog_cli_template.py`) を参考に実装
3. メニューシステムから始めて、段階的に機能を追加

### Step 4: 技術比較と理解深化
1. `orm_comparison.md` を読んで他言語のORMと比較
2. SQLAlchemy の強みと弱みを理解
3. 実際のプロジェクトでの選択基準を考察

## 次のステップ（今後の学習課題）

### Alembic（マイグレーション）学習
- [ ] Alembic の初期化と設定
- [ ] マイグレーションファイルの作成
- [ ] スキーマ変更の管理
- [ ] マイグレーションの実行とロールバック

### より高度な SQLAlchemy 機能
- [ ] カスタムクエリメソッド
- [ ] イベントリスナー
- [ ] バルク操作（一括挿入・更新）
- [ ] パフォーマンス最適化

### 統合学習
- [ ] FastAPI との連携
- [ ] Webアプリケーションでの実践
- [ ] テスト駆動開発（pytest + SQLAlchemy）

## 生成されるファイル
- `blog.db` - SQLiteデータベースファイル（`.gitignore`で除外済み）

## 重要な学習ポイント

1. **セッション管理**: SQLAlchemyでは明示的なセッション管理が重要
2. **型安全性**: `Mapped`と`mapped_column`による型安全なモデル定義
3. **リレーション**: `relationship`と`back_populates`による双方向関係
4. **クエリ最適化**: Eager loading（`joinedload`）や適切なインデックス
5. **エラーハンドリング**: `SQLAlchemyError`による適切な例外処理

このフェーズを通じて、Pythonでのデータベース操作の基礎から実践的なアプリケーション構築まで、包括的に学習できます。
