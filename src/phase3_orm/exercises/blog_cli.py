#!/usr/bin/env python3
"""
ブログ管理CLIアプリケーション - 演習課題

このファイルでは以下を実装してください：
- インタラクティブなメニューシステム
- ユーザー、カテゴリ、記事の管理機能
- 入力検証とエラーハンドリング

実装のヒント:
- テンプレートファイル (blog_cli_template.py) を参考にしてください
- 段階的に機能を追加していってください
- 最初はメニュー表示から始めることをお勧めします
"""

import argparse
import sys
from typing import Optional, List
from datetime import datetime

# 絶対インポートに変更
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import init_database
from crud_operations import UserCRUD, CategoryCRUD, PostCRUD
from models import User, Category, Post, Tag


class BlogCLI:
    """ブログ管理CLIアプリケーション"""
    
    def __init__(self):
        """CLIアプリケーションを初期化"""
        print("🚀 ブログ管理CLIアプリケーション")
        print("=" * 40)
        
        # データベース初期化
        init_database()
    
    def show_main_menu(self) -> None:
        """
        メインメニューを表示
        
        課題: この関数を実装してください
        - メニュー選択肢の表示
        - 適切な番号付け
        - 終了オプション
        """
        print("\\n📋 メニュー:")
        # TODO: メニュー項目を実装してください
        # 例: 1. ユーザー管理, 2. カテゴリ管理, 3. 記事管理, etc.
        pass
    
    def run_interactive(self) -> None:
        """
        インタラクティブモードでアプリケーションを実行
        
        課題: この関数を実装してください
        - メニューの表示と選択の受付
        - 各機能への分岐処理
        - 継続/終了の制御
        """
        # TODO: ここを実装してください
        # ヒント: while ループでメニューを繰り返し表示
        pass
    
    # ユーザー管理機能
    def user_management_menu(self) -> None:
        """
        ユーザー管理メニュー
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    def create_user_interactive(self) -> None:
        """
        インタラクティブなユーザー作成
        
        課題: この関数を実装してください
        - ユーザー名、メール、表示名の入力受付
        - 入力検証（空文字チェック、メール形式など）
        - 作成結果の表示
        """
        # TODO: ここを実装してください
        pass
    
    def list_users(self) -> None:
        """
        ユーザー一覧表示
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    # カテゴリ管理機能
    def category_management_menu(self) -> None:
        """
        カテゴリ管理メニュー
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    def create_category_interactive(self) -> None:
        """
        インタラクティブなカテゴリ作成
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    def list_categories(self) -> None:
        """
        カテゴリ一覧表示
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    # 記事管理機能
    def post_management_menu(self) -> None:
        """
        記事管理メニュー
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    def create_post_interactive(self) -> None:
        """
        インタラクティブな記事作成
        
        課題: この関数を実装してください
        - タイトル、スラッグ、コンテンツ等の入力
        - 著者・カテゴリの選択
        - 公開/非公開の選択
        """
        # TODO: ここを実装してください
        pass
    
    def list_posts(self) -> None:
        """
        記事一覧表示
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    def search_posts_interactive(self) -> None:
        """
        インタラクティブな記事検索
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        pass
    
    # ユーティリティ関数
    def get_user_input(self, prompt: str, required: bool = True) -> str:
        """
        ユーザー入力を取得
        
        課題: この関数を実装してください
        - 適切なプロンプト表示
        - 必須入力の検証
        - 空文字やスペースのみの入力の処理
        
        Args:
            prompt: 入力プロンプト
            required: 必須入力かどうか
            
        Returns:
            ユーザーの入力文字列
        """
        # TODO: ここを実装してください
        return ""
    
    def get_integer_input(self, prompt: str, min_val: int = 0) -> Optional[int]:
        """
        整数入力を取得
        
        課題: この関数を実装してください
        - 数値変換エラーの処理
        - 範囲チェック
        """
        # TODO: ここを実装してください
        return None
    
    def confirm_action(self, message: str) -> bool:
        """
        確認メッセージを表示し、Y/Nで応答を取得
        
        課題: この関数を実装してください
        """
        # TODO: ここを実装してください
        return False


def main():
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
        
        if args.interactive:
            cli.run_interactive()
        else:
            print("💡 --interactive オプションでインタラクティブモードを開始してください")
            print("例: python blog_cli.py --interactive")
            
    except KeyboardInterrupt:
        print("\\n\\n👋 アプリケーションを終了します")
        sys.exit(0)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
