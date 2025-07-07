"""
Alembicマイグレーション実習用モデル追加

このファイルでは、段階的にモデルを追加/変更して、
実際のマイグレーションを体験できるようにします。

実習の進め方:
1. このファイルの内容を確認
2. 必要に応じてmodels.pyに追加
3. マイグレーションファイルを生成
4. マイグレーションを実行
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column  # type: ignore
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List
from database import Base


# 実習1: 新しいテーブルの追加
class Comment(Base):
    """コメントモデル - 実習1で追加するテーブル"""
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
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # 作成日時
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 外部キー: 記事への参照
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    
    # リレーション
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, author='{self.author_name}', approved={self.is_approved})>"
    
    def __str__(self) -> str:
        return f"Comment by {self.author_name}"


# 実習2用: 既存のUserモデルに追加するカラム
# 以下のカラムをUserモデルに追加します:
"""
# プロフィール画像URL
profile_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

# 最後のログイン日時
last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

# ユーザーの説明文
bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# SNSリンク
twitter_handle: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
github_username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
"""


# 実習3: より複雑なテーブル - タグ統計テーブル
class TagStats(Base):
    """タグ統計モデル - 実習3で追加する集計テーブル"""
    __tablename__ = "tag_stats"
    
    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 外部キー: タグへの参照
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    
    # 使用回数
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # 最後の使用日時
    last_used: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # 統計更新日時
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # リレーション
    tag = relationship("Tag", back_populates="stats")
    
    # インデックス
    __table_args__ = (
        Index('idx_tag_stats_usage', 'usage_count'),
        Index('idx_tag_stats_last_used', 'last_used'),
    )
    
    def __repr__(self) -> str:
        return f"<TagStats(id={self.id}, tag_id={self.tag_id}, usage_count={self.usage_count})>"


# 実習4: セッション管理テーブル
class UserSession(Base):
    """ユーザーセッション管理モデル"""
    __tablename__ = "user_sessions"
    
    # 主キー
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # セッションID
    session_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    # 外部キー: ユーザーへの参照
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # IPアドレス
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6対応
    
    # ユーザーエージェント
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 作成日時
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 最終アクセス日時
    last_accessed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 有効期限
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # アクティブフラグ
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # リレーション
    user = relationship("User", back_populates="sessions")
    
    # インデックス
    __table_args__ = (
        Index('idx_user_sessions_user_id', 'user_id'),
        Index('idx_user_sessions_expires', 'expires_at'),
        Index('idx_user_sessions_active', 'is_active'),
    )
    
    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, user_id={self.user_id}, active={self.is_active})>"


# 既存モデルへの追加リレーション
# 以下のリレーションを既存モデルに追加することを想定:
"""
# Postモデルに追加
comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

# Userモデルに追加
sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

# Tagモデルに追加
stats = relationship("TagStats", back_populates="tag", uselist=False)
"""


def print_migration_models():
    """追加予定のモデル情報を表示"""
    print("🔧 Alembicマイグレーション実習用モデル")
    print("=" * 50)
    
    models = [
        ("Comment", "記事のコメント機能"),
        ("TagStats", "タグ使用統計"),
        ("UserSession", "ユーザーセッション管理"),
    ]
    
    for model_name, description in models:
        print(f"📝 {model_name}: {description}")
    
    print("\n💡 実習の進め方:")
    print("1. models.pyにモデルを段階的に追加")
    print("2. 各段階でマイグレーションファイルを生成")
    print("3. マイグレーションを実行してテーブル作成")
    print("4. 必要に応じてロールバックを実行")
    
    print("\n⚠️  注意事項:")
    print("- 既存のデータベースファイルをバックアップ")
    print("- マイグレーション実行前に必ず内容を確認")
    print("- 本番環境では慎重にテストしてから実行")


if __name__ == "__main__":
    print_migration_models()
