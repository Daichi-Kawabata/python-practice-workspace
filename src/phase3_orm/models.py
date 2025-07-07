"""
SQLAlchemy モデル定義

このファイルでは以下の概念を学習します：
- SQLAlchemyのモデル（テーブル）定義
- 主キー、外部キー、インデックスの設定
- 関係性（リレーション）の定義
- バリデーション、デフォルト値
- __repr__ メソッドによる表示設定
"""

from sqlalchemy import Table
from database import Base
from datetime import datetime
from typing import List, Optional, cast
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean, Index, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column  # type: ignore

# 絶対インポートでBase クラスをインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class User(Base):
    """ユーザーモデル

    ブログの著者を表現するモデル
    一人のユーザーは複数の記事を書くことができる（1対多の関係）
    """
    __tablename__ = "users"

    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ユーザー名（必須、ユニーク）
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False)

    # メールアドレス（必須、ユニーク）
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False)

    # 表示名（オプショナル）
    display_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)

    # アクティブフラグ
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    # 作成日時（自動設定）
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # 更新日時（自動更新）
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 実習2: 追加カラム（Alembicマイグレーション実習用）
    # プロフィール画像URL
    profile_image: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)

    # 最後のログイン日時
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True)

    # ユーザーの説明文
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # リレーション: 1人のユーザーは複数の記事を持つ
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"  # ユーザー削除時に関連記事も削除
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def __str__(self) -> str:
        return f"{self.display_name or self.username} ({self.email})"


class Category(Base):
    """カテゴリモデル

    ブログ記事のカテゴリを表現するモデル
    一つのカテゴリは複数の記事を持つことができる（1対多の関係）
    """
    __tablename__ = "categories"

    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # カテゴリ名（必須、ユニーク）
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False)

    # 説明文（オプショナル）
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # リレーション: 1つのカテゴリは複数の記事を持つ
    posts = relationship("Post", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return str(self.name)


class Post(Base):
    """記事モデル

    ブログの記事を表現するモデル
    一つの記事は一人の著者と一つのカテゴリに属する（多対1の関係）
    一つの記事は複数のタグを持つことができる（多対多の関係）
    """
    __tablename__ = "posts"

    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # タイトル（必須）
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)

    # スラッグ（URL用、ユニーク）
    slug: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False)

    # 本文（必須）
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 要約（オプショナル）
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 公開フラグ
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)

    # 公開日時（オプショナル）
    published_at: Mapped[Optional[datetime]
                         ] = mapped_column(DateTime, nullable=True)

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 外部キー: 著者への参照
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    # 外部キー: カテゴリへの参照
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False)

    # リレーション: 記事の著者
    author = relationship("User", back_populates="posts")

    # リレーション: 記事のカテゴリ
    category = relationship("Category", back_populates="posts")

    # リレーション: 記事のタグ（多対多）
    tags = relationship(
        "Tag",
        secondary="post_tags",  # 中間テーブル
        back_populates="posts"
    )

    # リレーション: 記事のコメント
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"  # 記事削除時に関連コメントも削除
    )

    # インデックス: 複合インデックスの例
    __table_args__ = (
        Index('idx_author_published', 'author_id', 'is_published'),
        Index('idx_category_published', 'category_id', 'is_published'),
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title='{self.title}', published={self.is_published})>"

    def __str__(self) -> str:
        return f"{self.title}"


class Tag(Base):
    """タグモデル

    記事に付けるタグを表現するモデル
    一つのタグは複数の記事に関連付けられる（多対多の関係）
    """
    __tablename__ = "tags"

    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # タグ名（必須、ユニーク）
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False)

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # リレーション: タグが付けられた記事（多対多）
    posts = relationship(
        "Post",
        secondary="post_tags",  # 中間テーブル
        back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return str(self.name)


class Comment(Base):
    """コメントモデル - Alembicマイグレーション実習用

    記事に対するコメントを管理するモデル
    """
    __tablename__ = "comments"

    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # コメント内容
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 投稿者名
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # 投稿者メールアドレス
    author_email: Mapped[str] = mapped_column(String(100), nullable=False)

    # 承認フラグ
    is_approved: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # 外部キー: 記事への参照
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False)

    # リレーション
    post = relationship("Post", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, author='{self.author_name}', approved={self.is_approved})>"

    def __str__(self) -> str:
        return f"Comment by {self.author_name}"


# 多対多の関係のための中間テーブル

post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    # 複合主キーにより、同じ記事に同じタグが重複して付けられることを防ぐ
)

# モデルの使用例とテスト用コード
if __name__ == "__main__":
    print("🔧 SQLAlchemyモデルテスト")

    from database import init_database, get_db_session

    try:
        # データベース初期化（テーブル作成）
        init_database()

        # テストデータ作成
        with get_db_session() as session:
            # ユーザー作成
            user = User(
                username="testuser",
                email="test@example.com",
                display_name="テストユーザー"
            )

            # カテゴリ作成
            category = Category(
                name="技術",
                description="技術関連の記事"
            )

            # タグ作成
            tag1 = Tag(name="Python")
            tag2 = Tag(name="SQLAlchemy")

            # 記事作成
            post = Post(
                title="SQLAlchemy入門",
                slug="sqlalchemy-introduction",
                content="SQLAlchemyの基本的な使い方について説明します。",
                summary="SQLAlchemy の基本",
                is_published=True,
                published_at=datetime.utcnow(),
                author=user,
                category=category,
                tags=[tag1, tag2]
            )

            # コメント作成
            comment1 = Comment(
                content="素晴らしい記事ですね！",
                author_name="山田太郎",
                author_email="taro.yamada@example.com",
                is_approved=True,
                post=post  # 記事に関連付け
            )

            comment2 = Comment(
                content="もっと詳しく知りたいです。",
                author_name="鈴木花子",
                author_email="hanako.suzuki@example.com",
                is_approved=False,
                post=post  # 記事に関連付け
            )

            # セッションに追加
            session.add_all([user, category, tag1, tag2,
                            post, comment1, comment2])
            session.commit()

            print("✅ テストデータ作成完了")
            print(f"ユーザー: {user}")
            print(f"記事: {post}")

            # セッション内でのタグアクセス（型アサーション使用）
            session.refresh(post)  # リレーションを再読み込み
            post_tags = cast(List[Tag], post.tags)  # 型アサーション
            if post_tags:
                tag_names = [str(tag) for tag in post_tags]
                print(f"タグ: {tag_names}")
            else:
                print("タグ: なし")

            # コメントの確認（型アサーション使用）
            post_comments = cast(List[Comment], post.comments)
            if post_comments:
                for comment in post_comments:
                    print(
                        f"コメント: {comment.content} (投稿者: {comment.author_name}, 承認済み: {comment.is_approved})")
            else:
                print("コメント: なし")

    except Exception as e:
        print(f"❌ エラー: {e}")
