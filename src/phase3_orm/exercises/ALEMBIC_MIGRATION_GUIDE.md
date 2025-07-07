# Alembicマイグレーション実習ガイド

このガイドでは、Alembicを使用したデータベーススキーマの変更管理を実践的に学習します。

## 🎯 学習目標

- [ ] Alembicの基本概念を理解する
- [ ] マイグレーションファイルの作成方法を学ぶ
- [ ] データベーススキーマの変更を安全に管理する
- [ ] マイグレーションの実行とロールバックを体験する

## 📋 前提条件

- SQLAlchemyの基本的な知識
- データベースの基本概念
- Python開発環境の設定完了

## 🚀 実習の流れ

### Step 1: 現在の状態を確認

まず、現在のAlembicの状態を確認しましょう。

```bash
# 現在のリビジョンを確認
alembic current

# マイグレーション履歴を確認
alembic history
```

### Step 2: 実習用プログラムの実行

```bash
# 実習用プログラムを実行
python exercises/alembic_migration_practice.py
```

### Step 3: 実習1 - 新しいテーブルの追加

#### 3.1 Commentモデルの追加

`models.py`にCommentモデルを追加します：

```python
class Comment(Base):
    """コメントモデル"""
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_email: Mapped[str] = mapped_column(String(100), nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 外部キー
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    
    # リレーション
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, author='{self.author_name}')>"
```

#### 3.2 Postモデルにリレーションを追加

```python
# Postモデルに追加
comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
```

#### 3.3 マイグレーションファイルの生成

```bash
alembic revision --autogenerate -m "Add Comment table"
```

#### 3.4 マイグレーションの実行

```bash
alembic upgrade head
```

### Step 4: 実習2 - 既存テーブルへのカラム追加

#### 4.1 Userモデルにカラムを追加

```python
# Userモデルに以下のカラムを追加
profile_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
```

#### 4.2 マイグレーションファイルの生成

```bash
alembic revision --autogenerate -m "Add user profile fields"
```

#### 4.3 マイグレーションの実行

```bash
alembic upgrade head
```

### Step 5: 実習3 - インデックスの追加

#### 5.1 手動でマイグレーションファイルを作成

```bash
alembic revision -m "Add performance indexes"
```

#### 5.2 マイグレーションファイルを編集

生成されたマイグレーションファイルを編集してインデックスを追加：

```python
def upgrade():
    # 複合インデックスの作成
    op.create_index(
        'idx_comments_post_created',
        'comments',
        ['post_id', 'created_at']
    )
    
    # 単一カラムインデックスの作成
    op.create_index(
        'idx_comments_approved',
        'comments',
        ['is_approved']
    )

def downgrade():
    op.drop_index('idx_comments_approved', table_name='comments')
    op.drop_index('idx_comments_post_created', table_name='comments')
```

#### 5.3 マイグレーションの実行

```bash
alembic upgrade head
```

### Step 6: 実習4 - ロールバックの実践

#### 6.1 現在の状態確認

```bash
alembic current
alembic history
```

#### 6.2 1つ前のバージョンに戻す

```bash
alembic downgrade -1
```

#### 6.3 再度最新バージョンに更新

```bash
alembic upgrade head
```

#### 6.4 特定のリビジョンに移動

```bash
# 特定のリビジョンIDに移動
alembic upgrade <revision_id>

# 初期状態に戻す
alembic downgrade base
```

## 🔧 よく使うAlembicコマンド

| コマンド | 説明 |
|---------|------|
| `alembic current` | 現在のリビジョンを表示 |
| `alembic history` | マイグレーション履歴を表示 |
| `alembic revision -m "message"` | 空のマイグレーションファイルを作成 |
| `alembic revision --autogenerate -m "message"` | 自動生成マイグレーションファイルを作成 |
| `alembic upgrade head` | 最新バージョンにアップグレード |
| `alembic upgrade +1` | 1つ先のバージョンにアップグレード |
| `alembic downgrade -1` | 1つ前のバージョンにダウングレード |
| `alembic downgrade base` | 初期状態にダウングレード |

## 🎯 実習課題

### 課題1: TagStatsテーブルの追加

`migration_models.py`を参考に、TagStatsモデルを追加してください。

**要件**:
- [ ] TagStatsモデルをmodels.pyに追加
- [ ] 適切なリレーションの設定
- [ ] マイグレーションファイルの生成と実行

### 課題2: UserSessionテーブルの追加

ユーザーセッション管理のためのテーブルを追加してください。

**要件**:
- [ ] UserSessionモデルをmodels.pyに追加
- [ ] 適切なインデックスの設定
- [ ] マイグレーションファイルの生成と実行

### 課題3: パフォーマンス最適化

既存のテーブルにパフォーマンス向上のためのインデックスを追加してください。

**要件**:
- [ ] 手動でマイグレーションファイルを作成
- [ ] 複合インデックスの追加
- [ ] マイグレーションの実行とテスト

## 🚨 注意事項

### 本番環境での注意点

1. **バックアップの取得**
   - マイグレーション実行前に必ずデータベースをバックアップ

2. **テスト環境での検証**
   - 本番環境で実行する前に必ずテスト環境で検証

3. **段階的な実行**
   - 大量のデータがある場合は、段階的にマイグレーションを実行

4. **ロールバック計画**
   - 問題が発生した場合のロールバック計画を事前に策定

### トラブルシューティング

#### マイグレーションファイルが生成されない場合

```bash
# Alembicがモデルの変更を検出できない場合
# models.pyのインポートを確認
# alembic/env.pyの設定を確認
```

#### マイグレーション実行エラー

```bash
# エラーの詳細を確認
alembic upgrade head --verbose

# SQL文のみ表示（実際には実行しない）
alembic upgrade head --sql
```

## 📚 参考資料

- [Alembic公式ドキュメント](https://alembic.sqlalchemy.org/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [データベースマイグレーションのベストプラクティス](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html)

## ✅ 完了チェックリスト

実習完了後、以下の項目をチェックしてください：

- [ ] Alembicの基本コマンドを理解している
- [ ] 新しいテーブルの追加ができる
- [ ] 既存テーブルへのカラム追加ができる
- [ ] インデックスの作成ができる
- [ ] マイグレーションの実行とロールバックができる
- [ ] マイグレーションファイルの内容を理解している
- [ ] 本番環境での注意点を理解している

頑張って実習を進めてください！🎉
