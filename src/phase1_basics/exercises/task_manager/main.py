import sys
from utils import CLIUtils
from services.task_manager import TaskManagerService

def main():
    manager = TaskManagerService()

    if len(sys.argv) < 2:
        print("使用法: python main.py <command> [args...]")
        print("コマンド: list, add, complete, delete")
        sys.exit(1)

    match sys.argv[1]:
        # python main.py listを想定
        case "list":
            tasks = manager.list_tasks()
            CLIUtils.display_tasks_table(tasks)
        # python main.py add タイトル [説明]を想定
        case "add":
            title = sys.argv[2]
            description = sys.argv[3] if len(sys.argv) > 3 else ""
            manager.add_task(title, description)
            CLIUtils.show_success(f"タスク {title} が追加されました")
        # python main.py complete タスクIDを想定
        case "complete":
            task_id = sys.argv[2]
            if CLIUtils.confirm_action(f"本当にタスク {task_id} を完了しますか？"):
                if manager.complete_task(task_id):
                    CLIUtils.show_success(f"タスク {task_id} が完了しました")
                else:
                    print(f"❌ タスク {task_id} が見つかりません")
        # python main.py delete タスクIDを想定
        case "delete":
            task_id = sys.argv[2]
            if CLIUtils.confirm_action(f"本当にタスク {task_id} を削除しますか？ (y/N): "):
                if manager.delete_task(task_id):
                    CLIUtils.show_success(f"タスク {task_id} が削除されました")
                else:
                    print(f"❌ タスク {task_id} が見つかりません")

if __name__ == "__main__":
    main()