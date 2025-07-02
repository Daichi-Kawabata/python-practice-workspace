from models import Task 
from typing import List

class CLIUtils:
    """
    CLIUtilsクラスは、タスク管理アプリケーションのCLIで使用するユーティリティ関数を提供します。
    """

    @staticmethod
    def display_tasks_table(tasks: List[Task]):
        """
        タスクの一覧をテーブル形式で表示する関数

        :param tasks: タスクのリスト
        """
        print("┌─────┬──────────┬──────────┬────────┬────────────┬────────────┐")
        print("│ ID  │ タイトル │ 説明     │ 状態   │ 作成日     │ 完了日     │")
        print("├─────┼──────────┼──────────┼────────┼────────────┼────────────┤")
        
        for task in tasks:
            status = "✅ 完了" if task.completed_at else "⏳ 未完了"
            created_date = str(task.created_at) if task.created_at else "-"
            completed_date = str(task.completed_at) if task.completed_at else "-"
            print(f"│ {task.id:<3} │ {task.title:<8} │ {task.description:<8} │ {status:<6} │ {created_date:<10} │ {completed_date:<10} │")
        
        print("└─────┴──────────┴──────────┴────────┴────────────┴────────────┘")

    @staticmethod
    def show_success(message):
        """
        成功メッセージを表示する関数

        :param message: 表示するメッセージ
        """
        print(f"\033[92m✅ {message}\033[0m")

    @staticmethod
    def confirm_action(message):
        """
        ユーザーにアクションの確認を求める関数

        :param message: 確認メッセージ
        :return: ユーザーの入力（True/False）
        """
        response = input(f"{message} (y/N): ").strip().lower()
        return response == 'y'