"""
SQLAlchemy モデル定義

このファイルでは以下の概念を学習します：
- SQLAlchemyのモデル（テーブル）定義
- 主キー、外部キー、インデックスの設定
- 関係性（リレーション）の定義
- バリデーション、デフォルト値
- __repr__ メソッドによる表示設定
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship, Mapped

# 絶対インポートでBase クラスをインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Base

class User(Base):
    """ユーザーモデル
    
    ブログの著者を表現するモデル
    一人のユーザーは複数の記事を書くことができる（1対多の関係）
    """
    __tablename__ = "users"
    
    # 主キー
    id = Column(Integer, primary_key=True, index=True)
    
    # ユーザー名（必須、ユニーク）
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # メールアドレス（必須、ユニーク）
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # 表示名（オプショナル）
    display_name = Column(String(100), nullable=True)
    
    # アクティブフラグ
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 作成日時（自動設定）
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 更新日時（自動更新）
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
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
    id = Column(Integer, primary_key=True, index=True)
    
    # カテゴリ名（必須、ユニーク）
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # 説明文（オプショナル）
    description = Column(Text, nullable=True)
    
    # 作成日時
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
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
    id = Column(Integer, primary_key=True, index=True)
    
    # タイトル（必須）
    title = Column(String(200), index=True, nullable=False)
    
    # スラッグ（URL用、ユニーク）
    slug = Column(String(200), unique=True, index=True, nullable=False)
    
    # 本文（必須）
    content = Column(Text, nullable=False)
    
    # 要約（オプショナル）
    summary = Column(Text, nullable=True)
    
    # 公開フラグ
    is_published = Column(Boolean, default=False, nullable=False)
    
    # 公開日時（オプショナル）
    published_at = Column(DateTime, nullable=True)
    
    # 作成日時
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 更新日時
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # 外部キー: 著者への参照
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 外部キー: カテゴリへの参照
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
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
    
    # インデックス: 複合インデックスの例
    __table_args__ = (
        Index('idx_author_published', 'author_id', 'is_published'),
        Index('idx_category_published', 'category_id', 'is_published'),
    )
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title='{self.title}', published={self.is_published})>"
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author.username if self.author else 'Unknown'}"

class Tag(Base):
    """タグモデル
    
    記事に付けるタグを表現するモデル
    一つのタグは複数の記事に関連付けられる（多対多の関係）
    """
    __tablename__ = "tags"
    
    # 主キー
    id = Column(Integer, primary_key=True, index=True)
    
    # タグ名（必須、ユニーク）
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # 作成日時
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
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

# 多対多の関係のための中間テーブル
from sqlalchemy import Table

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
            
            # セッションに追加
            session.add_all([user, category, tag1, tag2, post])
            session.commit()
            
            print("✅ テストデータ作成完了")
            print(f"ユーザー: {user}")
            print(f"記事: {post}")
            if post.tags:
                print(f"タグ: {[str(tag) for tag in post.tags]}")
            else:
                print("タグ: なし")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
