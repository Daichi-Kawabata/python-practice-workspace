#!/usr/bin/env python3
"""
ブログ管理CLIアプリケーション

このCLIアプリでは以下の機能を実装します：
- ユーザー管理（作成、一覧、更新、削除）
- カテゴリ管理（作成、一覧）
- 記事管理（作成、公開、検索、一覧）
- タグ管理
- インタラクティブなメニュー
"""

import argparse
import sys
from typing import Optional, List
from datetime import datetime

# 絶対インポートに変更
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import init_database
from crud_operations import UserCRUD, CategoryCRUD, PostCRUD
from models import User, Category, Post, Tag

class BlogCLI:
    """ブログ管理CLIアプリケーションのメインクラス"""
    
    def __init__(self) -> None:
        """CLIアプリケーションを初期化"""
        print("🚀 ブログ管理CLIアプリケーション")
        print("=" * 40)
        
        # データベース初期化
        init_database()
    
    def show_menu(self) -> None:
        """メインメニューを表示"""
        print("\n📋 メニュー:")
        print("1. ユーザー管理")
        print("2. カテゴリ管理") 
        print("3. 記事管理")
        print("4. 検索")
        print("5. 統計情報")
        print("0. 終了")
        print("-" * 20)
    
    def show_user_menu(self) -> None:
        """ユーザー管理メニューを表示"""
        print("\n👤 ユーザー管理:")
        print("1. ユーザー作成")
        print("2. ユーザー一覧")
        print("3. ユーザー情報更新")
        print("4. ユーザー削除")
        print("0. メインメニューに戻る")
        print("-" * 20)
    
    def show_category_menu(self) -> None:
        """カテゴリ管理メニューを表示"""
        print("\n📁 カテゴリ管理:")
        print("1. カテゴリ作成")
        print("2. カテゴリ一覧")
        print("0. メインメニューに戻る")
        print("-" * 20)
    
    def show_post_menu(self) -> None:
        """記事管理メニューを表示"""
        print("\n📝 記事管理:")
        print("1. 記事作成")
        print("2. 記事一覧（著者別）")
        print("3. 記事公開")
        print("4. 全記事一覧")
        print("0. メインメニューに戻る")
        print("-" * 20)
    
    def create_user(self) -> None:
        """ユーザーを作成"""
        print("\n👤 新しいユーザーを作成")
        
        username = input("ユーザー名: ").strip()
        if not username:
            print("❌ ユーザー名は必須です")
            return
        
        email = input("メールアドレス: ").strip()
        if not email:
            print("❌ メールアドレスは必須です")
            return
        
        display_name = input("表示名（オプション）: ").strip()
        display_name = display_name if display_name else None
        
        user = UserCRUD.create_user(username, email, display_name)
        if user:
            print(f"✅ ユーザー作成完了: {user}")
    
    def list_users(self) -> None:
        """ユーザー一覧を表示"""
        print("\n👥 ユーザー一覧")
        users = UserCRUD.get_all_users()
        
        if not users:
            print("ユーザーが見つかりません")
            return
        
        print(f"{'ID':<4} {'ユーザー名':<15} {'表示名':<15} {'メール':<25} {'アクティブ':<8}")
        print("-" * 75)
        
        for user in users:
            active_status = "✅" if user.is_active else "❌"
            print(f"{user.id:<4} {user.username:<15} {user.display_name or '':<15} {user.email:<25} {active_status:<8}")
    
    def update_user(self) -> None:
        """ユーザー情報を更新"""
        print("\n✏️ ユーザー情報更新")
        
        try:
            user_id = int(input("更新するユーザーID: "))
        except ValueError:
            print("❌ 無効なユーザーIDです")
            return
        
        user = UserCRUD.get_user_by_id(user_id)
        if not user:
            print(f"❌ ユーザーID {user_id} が見つかりません")
            return
        
        print(f"現在の情報: {user}")
        print("新しい値を入力してください（空の場合は変更なし）:")
        
        # 更新可能な項目
        display_name = input(f"表示名 [{user.display_name or ''}]: ").strip()
        is_active_input = input(f"アクティブ状態 (y/n) [{user.is_active}]: ").strip().lower()
        
        update_data = {}
        
        if display_name:
            update_data['display_name'] = display_name
        
        if is_active_input in ['y', 'n']:
            update_data['is_active'] = is_active_input == 'y'
        
        if update_data:
            updated_user = UserCRUD.update_user(user_id, **update_data)
            if updated_user:
                print(f"✅ ユーザー更新完了: {updated_user}")
        else:
            print("変更はありませんでした")
    
    def delete_user(self) -> None:
        """ユーザーを削除"""
        print("\n🗑️ ユーザー削除")
        
        try:
            user_id = int(input("削除するユーザーID: "))
        except ValueError:
            print("❌ 無効なユーザーIDです")
            return
        
        user = UserCRUD.get_user_by_id(user_id)
        if not user:
            print(f"❌ ユーザーID {user_id} が見つかりません")
            return
        
        print(f"削除対象: {user}")
        confirm = input("本当に削除しますか？ (y/N): ").strip().lower()
        
        if confirm == 'y':
            if UserCRUD.delete_user(user_id):
                print("✅ ユーザーを削除しました")
        else:
            print("削除をキャンセルしました")
    
    def create_category(self) -> None:
        """カテゴリを作成"""
        print("\n📁 新しいカテゴリを作成")
        
        name = input("カテゴリ名: ").strip()
        if not name:
            print("❌ カテゴリ名は必須です")
            return
        
        description = input("説明（オプション）: ").strip()
        description = description if description else None
        
        category = CategoryCRUD.create_category(name, description)
        if category:
            print(f"✅ カテゴリ作成完了: {category}")
    
    def list_categories(self) -> None:
        """カテゴリ一覧を表示"""
        print("\n📁 カテゴリ一覧")
        categories = CategoryCRUD.get_all_categories()
        
        if not categories:
            print("カテゴリが見つかりません")
            return
        
        print(f"{'ID':<4} {'名前':<20} {'説明':<40}")
        print("-" * 70)
        
        for category in categories:
            print(f"{category.id:<4} {category.name:<20} {category.description or '':<40}")
    
    def create_post(self) -> None:
        """記事を作成"""
        print("\n📝 新しい記事を作成")
        
        # 著者選択
        self.list_users()
        try:
            author_id = int(input("著者のユーザーID: "))
        except ValueError:
            print("❌ 無効なユーザーIDです")
            return
        
        # カテゴリ選択
        self.list_categories()
        try:
            category_id = int(input("カテゴリID: "))
        except ValueError:
            print("❌ 無効なカテゴリIDです")
            return
        
        # 記事情報入力
        title = input("タイトル: ").strip()
        if not title:
            print("❌ タイトルは必須です")
            return
        
        slug = input("スラッグ（URL用）: ").strip()
        if not slug:
            print("❌ スラッグは必須です")
            return
        
        content = input("本文: ").strip()
        if not content:
            print("❌ 本文は必須です")
            return
        
        summary = input("要約（オプション）: ").strip()
        summary = summary if summary else None
        
        # 公開設定
        is_published_input = input("公開しますか？ (y/N): ").strip().lower()
        is_published = is_published_input == 'y'
        
        # タグ入力
        tag_input = input("タグ（カンマ区切り、オプション）: ").strip()
        tag_names = [tag.strip() for tag in tag_input.split(",")] if tag_input else None
        
        post = PostCRUD.create_post(
            title=title,
            slug=slug,
            content=content,
            author_id=author_id,
            category_id=category_id,
            summary=summary,
            is_published=is_published,
            tag_names=tag_names
        )
        
        if post:
            print(f"✅ 記事作成完了: {post}")
    
    def list_posts_by_author(self) -> None:
        """著者別記事一覧"""
        print("\n📚 著者別記事一覧")
        
        self.list_users()
        try:
            author_id = int(input("著者のユーザーID: "))
        except ValueError:
            print("❌ 無効なユーザーIDです")
            return
        
        published_only = input("公開済みのみ表示？ (Y/n): ").strip().lower() != 'n'
        posts = PostCRUD.get_posts_by_author(author_id, published_only)
        
        if not posts:
            print("記事が見つかりません")
            return
        
        print(f"{'ID':<4} {'タイトル':<30} {'公開':<6} {'作成日':<12}")
        print("-" * 60)
        
        for post in posts:
            published_status = "✅" if post.is_published else "❌"
            created_date = post.created_at.strftime("%Y-%m-%d")
            print(f"{post.id:<4} {post.title[:30]:<30} {published_status:<6} {created_date:<12}")
    
    def search_posts(self) -> None:
        """記事を検索"""
        print("\n🔍 記事検索")
        
        keyword = input("キーワード: ").strip()
        if not keyword:
            print("❌ キーワードは必須です")
            return
        
        posts = PostCRUD.search_posts(keyword)
        
        if not posts:
            print("該当する記事が見つかりません")
            return
        
        print(f"🔍 検索結果: {len(posts)} 件")
        print(f"{'ID':<4} {'タイトル':<30} {'著者':<15} {'カテゴリ':<15}")
        print("-" * 70)
        
        for post in posts:
            author_name = post.author.username if post.author else "不明"
            category_name = post.category.name if post.category else "不明"
            print(f"{post.id:<4} {post.title[:30]:<30} {author_name:<15} {category_name:<15}")
    
    def run_user_management(self) -> None:
        """ユーザー管理を実行"""
        while True:
            self.show_user_menu()
            choice = input("選択: ").strip()
            
            if choice == "1":
                self.create_user()
            elif choice == "2":
                self.list_users()
            elif choice == "3":
                self.update_user()
            elif choice == "4":
                self.delete_user()
            elif choice == "0":
                break
            else:
                print("❌ 無効な選択です")
    
    def run_category_management(self) -> None:
        """カテゴリ管理を実行"""
        while True:
            self.show_category_menu()
            choice = input("選択: ").strip()
            
            if choice == "1":
                self.create_category()
            elif choice == "2":
                self.list_categories()
            elif choice == "0":
                break
            else:
                print("❌ 無効な選択です")
    
    def run_post_management(self) -> None:
        """記事管理を実行"""
        while True:
            self.show_post_menu()
            choice = input("選択: ").strip()
            
            if choice == "1":
                self.create_post()
            elif choice == "2":
                self.list_posts_by_author()
            elif choice == "0":
                break
            else:
                print("❌ 無効な選択です")
    
    def run(self) -> None:
        """メインループを実行"""
        while True:
            self.show_menu()
            choice = input("選択: ").strip()
            
            if choice == "1":
                self.run_user_management()
            elif choice == "2":
                self.run_category_management()
            elif choice == "3":
                self.run_post_management()
            elif choice == "4":
                self.search_posts()
            elif choice == "0":
                print("👋 ありがとうございました！")
                break
            else:
                print("❌ 無効な選択です")

def main() -> None:
    """メイン関数"""
    parser = argparse.ArgumentParser(description="ブログ管理CLIアプリケーション")
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="インタラクティブモードで実行"
    )
    
    args = parser.parse_args()
    
    try:
        cli = BlogCLI()
        
        if args.interactive or len(sys.argv) == 1:
            # インタラクティブモード
            cli.run()
        else:
            # コマンドラインモード（将来の拡張用）
            print("コマンドラインモードは未実装です。--interactive オプションを使用してください。")
            
    except KeyboardInterrupt:
        print("\n👋 アプリケーションを終了します")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
