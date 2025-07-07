"""
SQLAlchemy CRUD操作（Create, Read, Update, Delete）- 演習課題

このファイルでは以下を実装してください：
- ユーザー、カテゴリ、記事のCRUD操作
- セッション管理
- エラーハンドリング
- トランザクション処理

実装のヒント:
- テンプレートファイル (crud_operations_template.py) を参考にしてください
- 一つずつメソッドを実装し、動作確認をしながら進めてください
- SQLAlchemyのクエリ構文に慣れることが重要です
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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db_session
from models import User, Category, Post, Tag


class UserCRUD:
    """ユーザーのCRUD操作を行うクラス"""
    
    @staticmethod
    def create_user(username: str, email: str, display_name: Optional[str] = None) -> Optional[User]:
        """
        新しいユーザーを作成
        
        課題: この関数を実装してください
        - ユーザー重複チェック（username, email）
        - エラーハンドリング
        - セッション管理
        
        Args:
            username: ユーザー名（一意）
            email: メールアドレス（一意）
            display_name: 表示名（オプション）
            
        Returns:
            作成されたUserオブジェクト、失敗時はNone
        """
        try:
            with get_db_session() as session:
                existing_user = session.query(User).filter(
                    or_(User.username == username, User.email == email)
                ).first()
                if existing_user:
                    print(f"ユーザー名またはメールアドレスが既に存在します: {username}, {email}")
                    return None
                
                new_user = User(
                    username=username,
                    email=email,
                    display_name=display_name,
                )

                session.add(new_user)
                session.commit()

                print(f"ユーザー作成成功: {new_user}")

                return new_user
        except SQLAlchemyError as e:
            print(f"ユーザー作成エラー：{e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        IDでユーザーを取得
        
        課題: この関数を実装してください
        
        Args:
            user_id: ユーザーID
            
        Returns:
            Userオブジェクト、見つからない場合はNone
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    print(f"ユーザー取得成功: {user}")
                    return user
                else:
                    print(f"ユーザーが見つかりません: ID={user_id}")
                    return None
        except SQLAlchemyError as e:
            print(f"ユーザー取得エラー: {e}")
            return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """
        ユーザー名でユーザーを取得
        
        課題: この関数を実装してください
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.username == username).first()
                if user:
                    print(f"ユーザー取得成功：{user}")
                    return user
                else:
                    print(f"ユーザーが見つかりません：ユーザー名＝{username}")
                    return None
        except SQLAlchemyError as e:
            print(f"ユーザー取得エラー: {e}")
            return None
    
    @staticmethod
    def update_user(user_id: int, **kwargs) -> bool:
        """
        ユーザー情報を更新
        
        課題: この関数を実装してください
        - 更新可能フィールド: display_name, email, is_active
        - updated_at フィールドの自動更新
        
        Args:
            user_id: 更新対象のユーザーID
            **kwargs: 更新するフィールドと値
            
        Returns:
            更新成功時True、失敗時False
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    print(f"ユーザが見つかりません：ID={user_id}")
                    return False

                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                    else:
                        print(f"更新フィールドが無効です：{kwargs.keys()}")
                setattr(user, 'updated_at', datetime.utcnow())
                session.commit()
                print(f"ユーザー更新成功：{user}")
                return True
        except SQLAlchemyError as e:
            print(f"ユーザー更新エラー：{e}")
            return False
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        ユーザーを削除
        
        課題: この関数を実装してください
        - 関連する記事も削除するかどうか検討
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    print(f"ユーザーが見つかりません：ID={user_id}")
                    return False
                session.delete(user)
                session.commit()
                print(f"ユーザー削除成功：{user}")
                return True
        except SQLAlchemyError as e:
            print(f"ユーザー削除エラー：{e}")
            return False


class CategoryCRUD:
    """カテゴリのCRUD操作を行うクラス"""
    
    @staticmethod
    def create_category(name: str, description: Optional[str] = None) -> Optional[Category]:
        """
        新しいカテゴリを作成
        
        課題: この関数を実装してください
        """

        try:
            with get_db_session() as session:
                existing_category = session.query(Category).filter(Category.name == name).first()
                if existing_category:
                    print(f"カテゴリ名が既に存在しています。：{name}")
                    return None
                
                new_category = Category(
                    name=name,
                    description=description
                )
                session.add(new_category)
                session.commit()
                print(f"カテゴリの作成成功：{new_category}")
                return new_category
        except SQLAlchemyError as e:
            print(f"カテゴリー作成エラー：{e}")
            return None
    
    @staticmethod
    def get_all_categories() -> List[Category]:
        """
        すべてのカテゴリを取得
        
        課題: この関数を実装してください
        """
        try:
            with get_db_session() as session:
                categories = session.query(Category).all()
                print(f"全カテゴリの取得成功：{len(categories)}件")
                return categories
        except SQLAlchemyError as e:
            print(f"カテゴリ取得エラー：{e}")
            return []
    
    @staticmethod
    def get_category_by_name(name: str) -> Optional[Category]:
        """
        名前でカテゴリを取得
        
        課題: この関数を実装してください
        """
        
        try:
            with get_db_session() as session:
                category = session.query(Category).filter(Category.name == name).first()
                if category:
                    print(f"カテゴリの取得成功：{category}")
                    return category
                else:
                    print(f"カテゴリが見つかりません。名前 = {name}")
                    return None
        except SQLAlchemyError as e:
            print(f"カテゴリ取得エラー：{e}")
            return None


class PostCRUD:
    """記事のCRUD操作を行うクラス"""
    
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
        """
        新しい記事を作成
        
        課題: この関数を実装してください
        - タグの自動作成または既存タグとの関連付け
        - slug の重複チェック
        - published_at の設定（公開時のみ）
        """


        try:
            with get_db_session() as session:
                # 著者の存在チェック
                author = session.query(User).filter(User.id == author_id).first()
                if not author:
                    print(f"著者が見つかりません。ID：{author_id}")
                    return None

                # カテゴリチェック
                category = session.query(Category).filter(Category.id == category_id).first()
                if not category:
                    print(f"カテゴリが見つかりません。category_iod={category_id}")
                    return None

                # slugの重複チェック
                exsisting_post = session.query(Post).filter(Post.slug == slug).first()
                if exsisting_post:
                    print(f"スラッグが既に存在します。：{slug}")
                    return None
                
                # タグの自動作成、あれば関連付ける
                tags: List[Tag] = []
                if tag_names:
                    existing_tags = session.query(Tag).filter(Tag.name.in_(tag_names)).all()
                    existing_tag_names = {str(tag.name) for tag in existing_tags}

                    tags.extend(existing_tags)

                    new_tag_names = set(tag_names) - existing_tag_names
                    new_tags = [Tag(name=name) for name in new_tag_names]
                    if new_tags:
                        session.add_all(new_tags)
                        session.flush() # 新しいのタグのＩＤを取得する必要がある場合はflushを利用することで取得できる
                        tags.extend(new_tags)

                # 記事の作成
                new_post = Post(
                    title=title,
                    slug=slug,
                    content=content,
                    summary=summary,
                    is_published=is_published,
                    published_at=datetime.utcnow() if is_published else None,
                    author=author,
                    category=category,
                    tags=tags
                )
                session.add(new_post)
                session.commit()
                print(f"記事の作成成功：{new_post}")
                return new_post
        except SQLAlchemyError as e:
            print(f"記事作成エラー：{e}")
            return None

    
    @staticmethod
    def get_posts_by_author(author_id: int, published_only: bool = True) -> List[Post]:
        """
        著者IDで記事を取得
        
        課題: この関数を実装してください
        """
        try:
            with get_db_session() as session:
                posts = session.query(Post).filter(Post.author_id == author_id)
                if published_only:
                    posts = posts.filter(Post.is_published == True)

                return posts.all()
        except SQLAlchemyError as e:
            print(f"記事取得エラー：{e}")
            return []

    @staticmethod
    def search_posts(keyword: str, published_only: bool = True) -> List[Post]:
        """
        キーワードで記事を検索
        
        課題: この関数を実装してください
        - タイトル、コンテンツ、サマリーから検索
        - 大文字小文字を区別しない検索
        """
        try:
            with get_db_session() as session:
                query = session.query(Post)
                if published_only:
                    query = query.filter(Post.is_published == True)
                
                query = query.filter(
                    or_(
                        Post.title.ilike(f"%{keyword}%"),
                        Post.content.ilike(f"%{keyword}%"),
                        Post.summary.ilike(f"%{keyword}%")
                    )
                )

                return query.all()
        except SQLAlchemyError as e:
            print(f"記事検索エラー：{e}")
            return []
    
    @staticmethod
    def update_post(post_id: int, **kwargs) -> bool:
        """
        記事を更新
        
        課題: この関数を実装してください
        - updated_at の自動更新
        - is_published が True に変更された場合の published_at 設定
        """
        try:
            with get_db_session() as session:
                post = session.query(Post).filter(Post.id == post_id).first()
                if not post:
                    print(f"記事が見つかりません：ID={post_id}")
                    return False
                for key, value in kwargs.items():
                    if hasattr(post, key):
                        setattr(post, key, value)
                    else:
                        print(f"更新フィールドが無効です：{key}")
                setattr(post, 'updated_at', datetime.utcnow())
                if post.is_published and not post.published_at:
                    setattr(post, 'published_at', datetime.utcnow())

                session.commit()
                print(f"記事更新成功：{post}")
                return True
        except SQLAlchemyError as e:
            print(f"記事更新エラー：{e}")
            return False
            

    
    @staticmethod
    def delete_post(post_id: int) -> bool:
        """
        記事を削除
        
        課題: この関数を実装してください
        """
        try:
            with get_db_session() as session:
                post = session.query(Post).filter(Post.id == post_id).first()
                if not post:
                    print(f"記事が見つかりません：ID={post_id}")
                    return False
                
                post_title = post.title
                session.delete(post)
                session.commit()
                print(f"記事削除成功：{post_title}")
                return True
        except SQLAlchemyError as e:
            print(f"記事削除エラー：{e}")
            return False


# テスト用コード
if __name__ == "__main__":
    print("🔧 CRUD操作テスト - 演習課題")
    
    from database import init_database
    
    try:
        # データベース初期化
        init_database()

        new_user = UserCRUD.create_user(
            username= f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            email=f"example_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com")
        if new_user:
            print(f"ユーザーID検索確認 ID：{new_user.id}")
            # exist_user = UserCRUD.get_user_by_id(new_user.id)
            # if exist_user:
            #     print(f"取得したユーザー: {exist_user}")
            # else:
            #     print("ユーザーが見つかりません。")
            exist_user = UserCRUD.get_user_by_username(new_user.username)
            if exist_user:
                print(f"取得したユーザー: {exist_user.__repr__()}")
            else:
                print("ユーザーが見つかりません。")

            is_update = UserCRUD.update_user(
                user_id=new_user.id,
                display_name="更新ユーザー",
                email=f"updated_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
            )
            if is_update:
                print("ユーザー更新成功")
            
            # is_delete = UserCRUD.delete_user(new_user.id)
            # if is_delete:
            #     print("ユーザー削除成功")

            new_category = CategoryCRUD.create_category(
                name=f"技術-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                description="技術関連の記事"
            )
            if new_category:
                post = PostCRUD.create_post(
                    title="SQLAlchemy入門",
                    slug=f"sqlalchemy-introduction-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    content="SQLAlchemyの基本的な使い方について説明します。",
                    author_id=new_user.id,
                    category_id=new_category.id,
                    summary="SQLAlchemy の基本",
                    is_published=True,
                    tag_names=["Python", "SQLAlchemy"]
                )
                if post:
                    print(f"記事の作成成功: {post.title} (ID: {post.id})")
                    post_id = post.id  # post.idを保存
                    
                    # 記事の取得
                    posts = PostCRUD.get_posts_by_author(new_user.id)
                    print(f"著者ID {new_user.id} の記事数: {len(posts)}件")
                    
                    # 記事の検索
                    search_results = PostCRUD.search_posts("SQLAlchemy")
                    print(f"検索結果: {len(search_results)}件")
                    
                    # 記事の更新
                    is_updated = PostCRUD.update_post(post_id, title="SQLAlchemy入門 - 更新版", is_published=True)
                    if is_updated:
                        print("記事更新成功")
                    
                    # 記事の削除
                    is_deleted = PostCRUD.delete_post(post_id)
                    if is_deleted:
                        print("記事削除成功")
                else:
                    print("記事の作成に失敗しました。")
            else:
                print("カテゴリの作成に失敗したため、記事の作成をスキップします。")
            
        print("✅ テスト実行完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
