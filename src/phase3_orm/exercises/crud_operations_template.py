"""
SQLAlchemy CRUD操作（Create, Read, Update, Delete）

このファイルでは以下の概念を学習します：
- SQLAlchemyでのCRUD操作
- セッション管理
- クエリの実行
- エラーハンドリング
- トランザクション処理
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
from sqlalchemy.exc import SQLAlchemyError

# 絶対インポートに変更
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import get_db_session
from models import User, Category, Post, Tag

class UserCRUD:
    """ユーザーに関するCRUD操作クラス"""
    
    @staticmethod
    def create_user(
        username: str, 
        email: str, 
        display_name: Optional[str] = None
    ) -> Optional[User]:
        """新しいユーザーを作成
        
        Args:
            username: ユーザー名
            email: メールアドレス
            display_name: 表示名（オプション）
            
        Returns:
            作成されたUserオブジェクト、エラー時はNone
        """
        try:
            with get_db_session() as session:
                # 新しいUserインスタンスを作成
                user = User(
                    username=username,
                    email=email,
                    display_name=display_name
                )
                
                # セッションに追加
                session.add(user)
                # データベースにコミット
                session.commit()
                # オブジェクトを最新状態に更新
                session.refresh(user)
                
                print(f"✅ ユーザー作成成功: {user}")
                return user
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー作成エラー: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """IDでユーザーを取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            見つかったUserオブジェクト、見つからない場合はNone
        """
        try:
            with get_db_session() as session:
                # session.get() で主キーによる検索
                user = session.get(User, user_id)
                return user
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー取得エラー: {e}")
            return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得
        
        Args:
            username: ユーザー名
            
        Returns:
            見つかったUserオブジェクト、見つからない場合はNone
        """
        try:
            with get_db_session() as session:
                # session.query() でクエリを実行
                user = session.query(User).filter(User.username == username).first()
                return user
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー取得エラー: {e}")
            return None
    
    @staticmethod
    def get_all_users(limit: int = 100) -> List[User]:
        """全ユーザーを取得
        
        Args:
            limit: 取得件数の上限
            
        Returns:
            Userオブジェクトのリスト
        """
        try:
            with get_db_session() as session:
                users = session.query(User).limit(limit).all()
                return users
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー一覧取得エラー: {e}")
            return []
    
    @staticmethod
    def update_user(user_id: int, **kwargs) -> Optional[User]:
        """ユーザー情報を更新
        
        Args:
            user_id: ユーザーID
            **kwargs: 更新する値（display_name、is_activeなど）
            
        Returns:
            更新されたUserオブジェクト、エラー時はNone
        """
        try:
            with get_db_session() as session:
                user = session.get(User, user_id)
                if not user:
                    print(f"❌ ユーザーID {user_id} が見つかりません")
                    return None
                
                # 属性を動的に更新
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                
                session.commit()
                session.refresh(user)
                
                print(f"✅ ユーザー更新成功: {user}")
                return user
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー更新エラー: {e}")
            return None
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """ユーザーを削除
        
        Args:
            user_id: ユーザーID
            
        Returns:
            削除成功時True、エラー時False
        """
        try:
            with get_db_session() as session:
                user = session.get(User, user_id)
                if not user:
                    print(f"❌ ユーザーID {user_id} が見つかりません")
                    return False
                
                session.delete(user)
                session.commit()
                
                print(f"✅ ユーザー削除成功: ID {user_id}")
                return True
                
        except SQLAlchemyError as e:
            print(f"❌ ユーザー削除エラー: {e}")
            return False

class PostCRUD:
    """記事に関するCRUD操作クラス"""
    
    @staticmethod
    def create_post(
        title: str,
        slug: str,
        content: str,
        author_id: int,
        category_id: int,
        summary: Optional[str] = None,
        is_published: bool = False,
        tag_names: Optional[List[str]] = None
    ) -> Optional[Post]:
        """新しい記事を作成
        
        Args:
            title: タイトル
            slug: URL用スラッグ
            content: 本文
            author_id: 著者のユーザーID
            category_id: カテゴリID
            summary: 要約（オプション）
            is_published: 公開フラグ
            tag_names: タグ名のリスト（オプション）
            
        Returns:
            作成されたPostオブジェクト、エラー時はNone
        """
        try:
            with get_db_session() as session:
                # 記事作成
                post = Post(
                    title=title,
                    slug=slug,
                    content=content,
                    author_id=author_id,
                    category_id=category_id,
                    summary=summary,
                    is_published=is_published,
                    published_at=datetime.utcnow() if is_published else None
                )
                
                # タグの処理
                if tag_names:
                    tags = []
                    for tag_name in tag_names:
                        # 既存のタグを検索、なければ作成
                        tag = session.query(Tag).filter(Tag.name == tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            session.add(tag)
                        tags.append(tag)
                    
                    post.tags = tags
                
                session.add(post)
                session.commit()
                session.refresh(post)
                
                print(f"✅ 記事作成成功: {post}")
                return post
                
        except SQLAlchemyError as e:
            print(f"❌ 記事作成エラー: {e}")
            return None
    
    @staticmethod
    def get_posts_by_author(author_id: int, published_only: bool = True) -> List[Post]:
        """著者IDで記事を取得
        
        Args:
            author_id: 著者のユーザーID
            published_only: 公開済みのみ取得するかどうか
            
        Returns:
            Postオブジェクトのリスト
        """
        try:
            with get_db_session() as session:
                query = session.query(Post).filter(Post.author_id == author_id)
                
                if published_only:
                    query = query.filter(Post.is_published == True)
                
                # 作成日時の降順でソート
                posts = query.order_by(desc(Post.created_at)).all()
                return posts
                
        except SQLAlchemyError as e:
            print(f"❌ 記事取得エラー: {e}")
            return []
    
    @staticmethod
    def search_posts(
        keyword: str, 
        category_id: Optional[int] = None,
        tag_name: Optional[str] = None
    ) -> List[Post]:
        """記事を検索
        
        Args:
            keyword: タイトルまたは内容の検索キーワード
            category_id: カテゴリID（オプション）
            tag_name: タグ名（オプション）
            
        Returns:
            Postオブジェクトのリスト
        """
        try:
            with get_db_session() as session:
                query = session.query(Post).filter(Post.is_published == True)
                
                # キーワード検索（タイトルまたは内容に含まれる）
                if keyword:
                    query = query.filter(
                        or_(
                            Post.title.contains(keyword),
                            Post.content.contains(keyword)
                        )
                    )
                
                # カテゴリフィルター
                if category_id:
                    query = query.filter(Post.category_id == category_id)
                
                # タグフィルター
                if tag_name:
                    query = query.join(Post.tags).filter(Tag.name == tag_name)
                
                posts = query.order_by(desc(Post.published_at)).all()
                return posts
                
        except SQLAlchemyError as e:
            print(f"❌ 記事検索エラー: {e}")
            return []
    
    @staticmethod
    def publish_post(post_id: int) -> Optional[Post]:
        """記事を公開する
        
        Args:
            post_id: 記事ID
            
        Returns:
            更新されたPostオブジェクト、エラー時はNone
        """
        try:
            with get_db_session() as session:
                post = session.get(Post, post_id)
                if not post:
                    print(f"❌ 記事ID {post_id} が見つかりません")
                    return None
                
                post.is_published = True
                post.published_at = datetime.utcnow()
                
                session.commit()
                session.refresh(post)
                
                print(f"✅ 記事公開成功: {post}")
                return post
                
        except SQLAlchemyError as e:
            print(f"❌ 記事公開エラー: {e}")
            return None

class CategoryCRUD:
    """カテゴリに関するCRUD操作クラス"""
    
    @staticmethod
    def create_category(name: str, description: Optional[str] = None) -> Optional[Category]:
        """新しいカテゴリを作成
        
        Args:
            name: カテゴリ名
            description: 説明（オプション）
            
        Returns:
            作成されたCategoryオブジェクト、エラー時はNone
        """
        try:
            with get_db_session() as session:
                category = Category(name=name, description=description)
                session.add(category)
                session.commit()
                session.refresh(category)
                
                print(f"✅ カテゴリ作成成功: {category}")
                return category
                
        except SQLAlchemyError as e:
            print(f"❌ カテゴリ作成エラー: {e}")
            return None
    
    @staticmethod
    def get_all_categories() -> List[Category]:
        """全カテゴリを取得
        
        Returns:
            Categoryオブジェクトのリスト
        """
        try:
            with get_db_session() as session:
                categories = session.query(Category).order_by(Category.name).all()
                return categories
                
        except SQLAlchemyError as e:
            print(f"❌ カテゴリ一覧取得エラー: {e}")
            return []

# 使用例とテスト用コード
if __name__ == "__main__":
    print("🔧 CRUD操作テスト")
    
    from database import init_database
    
    try:
        # データベース初期化
        init_database()
        
        # ユーザー作成テスト
        user = UserCRUD.create_user(
            username="testuser",
            email="test@example.com",
            display_name="テストユーザー"
        )
        
        if user:
            # カテゴリ作成テスト
            category = CategoryCRUD.create_category(
                name="技術",
                description="技術関連の記事"
            )
            
            if category:
                # 記事作成テスト
                post = PostCRUD.create_post(
                    title="SQLAlchemy入門",
                    slug="sqlalchemy-introduction",
                    content="SQLAlchemyの基本的な使い方について説明します。",
                    author_id=user.id,
                    category_id=category.id,
                    summary="SQLAlchemyの基本",
                    is_published=True,
                    tag_names=["Python", "SQLAlchemy", "ORM"]
                )
                
                if post:
                    # 検索テスト
                    found_posts = PostCRUD.search_posts("SQLAlchemy")
                    print(f"🔍 検索結果: {len(found_posts)} 件")
                    
                    # ユーザーの記事取得テスト
                    user_posts = PostCRUD.get_posts_by_author(user.id)
                    print(f"📝 ユーザーの記事: {len(user_posts)} 件")
        
        print("✅ CRUD操作テスト完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
