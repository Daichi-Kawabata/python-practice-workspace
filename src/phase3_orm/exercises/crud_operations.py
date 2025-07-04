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
        # TODO: ここを実装してください
        pass
    
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
        # TODO: ここを実装してください
        pass
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """
        ユーザー名でユーザーを取得
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
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
        # TODO: ここを実装してください
        return False
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        ユーザーを削除
        
        課題: この関数を実装してください
        - 関連する記事も削除するかどうか検討
        """
        # TODO: ここを実装してください
        return False


class CategoryCRUD:
    """カテゴリのCRUD操作を行うクラス"""
    
    @staticmethod
    def create_category(name: str, description: Optional[str] = None) -> Optional[Category]:
        """
        新しいカテゴリを作成
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    @staticmethod
    def get_all_categories() -> List[Category]:
        """
        すべてのカテゴリを取得
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        return []
    
    @staticmethod
    def get_category_by_name(name: str) -> Optional[Category]:
        """
        名前でカテゴリを取得
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass


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
        # TODO: ここを実装してください
        pass
    
    @staticmethod
    def get_posts_by_author(author_id: int, published_only: bool = True) -> List[Post]:
        """
        著者IDで記事を取得
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        return []
    
    @staticmethod
    def search_posts(keyword: str, published_only: bool = True) -> List[Post]:
        """
        キーワードで記事を検索
        
        課題: この関数を実装してください
        - タイトル、コンテンツ、サマリーから検索
        - 大文字小文字を区別しない検索
        """
        # TODO: ここを実装してください
        return []
    
    @staticmethod
    def update_post(post_id: int, **kwargs) -> bool:
        """
        記事を更新
        
        課題: この関数を実装してください
        - updated_at の自動更新
        - is_published が True に変更された場合の published_at 設定
        """
        # TODO: ここを実装してください
        return False
    
    @staticmethod
    def delete_post(post_id: int) -> bool:
        """
        記事を削除
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        return False


# テスト用コード
if __name__ == "__main__":
    print("🔧 CRUD操作テスト - 演習課題")
    
    from database import init_database
    
    try:
        # データベース初期化
        init_database()
        
        # TODO: 実装したメソッドをテストしてください
        
        print("✅ テスト実行完了")
        print("💡 各メソッドを実装後、ここでテストしてください")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
