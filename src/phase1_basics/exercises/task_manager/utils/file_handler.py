import json
import os
from typing import List

from models import Task

import pdb  # デバッグ用のインポート

class FileHandler:
    """
    ファイル操作を担当するクラス
    """
    
    @staticmethod
    def load_tasks_from_json(file_path: str) -> List[Task]:
        """
        JSONファイルからタスクを読み込む
        
        :param file_path: JSONファイルのパス
        :return: タスクのリスト
        """
        # 絶対パスに変換
        if not os.path.isabs(file_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)  # task_manager/ディレクトリ
            file_path = os.path.join(project_root, file_path)
                
        if not os.path.exists(file_path):
            # ファイルが存在しない場合は空のファイルを作成
            FileHandler.save_tasks_to_json([], file_path)
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                return [Task(**task) for task in tasks_data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    @staticmethod
    def save_tasks_to_json(tasks: List[Task], file_path: str) -> None:
        """
        タスクをJSONファイルに保存する
        
        :param tasks: 保存するタスクのリスト
        :param file_path: 保存先のファイルパス
        """
        # 絶対パスに変換（load_tasks_from_jsonと同じ処理）
        if not os.path.isabs(file_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)  # task_manager/ディレクトリ
            file_path = os.path.join(project_root, file_path)
                
        tasks_data = []
        for task in tasks:
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': str(task.created_at) if task.created_at else None,
                'completed_at': str(task.completed_at) if task.completed_at else None
            }
            tasks_data.append(task_dict)
        
        # ディレクトリが存在しない場合は作成
        dir_path = os.path.dirname(file_path)
        if dir_path:  # ディレクトリパスが空でない場合のみ作成
            os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)