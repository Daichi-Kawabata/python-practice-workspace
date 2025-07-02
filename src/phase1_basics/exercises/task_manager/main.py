import pdb
import sys
from utils import CLIUtils
from services.task_manager import TaskManagerService

import pdb

def main():
    manager = TaskManagerService()


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
                manager.complete_task(task_id)
                CLIUtils.show_success(f"タスク {task_id} が完了しました")
        # python main.py delete タスクIDを想定
        case "delete":
            task_id = sys.argv[2]
            if CLIUtils.confirm_action(f"本当にタスク {task_id} を削除しますか？ (y/N): "):
                manager.delete_task(task_id)
                CLIUtils.show_success(f"タスク {task_id} が削除されました")

if __name__ == "__main__":
    main()