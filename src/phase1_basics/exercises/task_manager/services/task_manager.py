
import random
import string
from datetime import date

from models import Task
from utils import FileHandler

class TaskManagerService:
    """
    タスク管理サービスクラス
    """

    def __init__(self, data_file: str = "tasks.json"):
        """
        コンストラクタ
        """
        self.data_file: str = data_file
        self.tasks: list[Task] = []
        self._load_tasks()

    def _load_tasks(self) -> None:
        """
        JSONファイルからタスクを読み込む
        """

        self.tasks = FileHandler.load_tasks_from_json(self.data_file)

    
    def _save_tasks(self) -> None:
        """
        タスクをJSONファイルに保存する
        """
        FileHandler.save_tasks_to_json(self.tasks, self.data_file)

    def add_task(self, title: str, description: str = "") -> None:
        """
        タスクを追加する

        :param title: タスクのタイトル
        :param description: タスクの説明（オプション）
        """


        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # タスクを作成
        new_task = Task(
            id=task_id,
            title=title,
            description=description,
            created_at=date.today(),
            completed_at=None
        )

        # タスクをリストに追加してJSONファイルに保存
        self.tasks.append(new_task)
        self._save_tasks()
        


    def list_tasks(self) -> list[Task]:
        """
        タスクの一覧を取得するメソッド

        :return: タスクのリスト
        """
        return self.tasks
    
    def complete_task(self, task_id: str) -> bool:
        """
        タスクを完了するメソッド

        :param task_id: 完了するタスクのID
        """
        for task in self.tasks:
            if task.id == task_id:
                task.completed_at = date.today()
                self._save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        タスクを削除するメソッド

        :param task_id: 削除するタスクのID
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self._save_tasks()
                return True
        return False