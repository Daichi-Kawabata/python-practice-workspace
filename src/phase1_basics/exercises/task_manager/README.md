# タスク管理CLIツール

## 課題1の実装場所

このディレクトリに以下の構成でタスク管理CLIツールを実装してください。

### 実装すべきファイル構成
```
task_manager/
├── main.py              # メインエントリーポイント
├── models/
│   ├── __init__.py
│   └── task.py          # Taskクラス
├── services/
│   ├── __init__.py
│   └── task_manager.py  # TaskManagerクラス
├── utils/
│   ├── __init__.py
│   ├── file_handler.py  # ファイル操作
│   └── cli_utils.py     # CLI用ユーティリティ
└── tasks.json           # データファイル（自動生成）
```

### ヒント

#### Taskクラス (models/task.py)
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    # TODO: タスクの属性を定義
    # id, title, description, completed, created_at, completed_at
    pass
```

#### TaskManagerクラス (services/task_manager.py)
```python
from typing import List, Optional
from models.task import Task

class TaskManager:
    def __init__(self, data_file: str = "tasks.json"):
        # TODO: 初期化処理
        pass
    
    def add_task(self, title: str, description: str = "") -> Task:
        # TODO: タスク追加
        pass
    
    def list_tasks(self) -> List[Task]:
        # TODO: タスク一覧取得
        pass
    
    def complete_task(self, task_id: int) -> bool:
        # TODO: タスク完了
        pass
    
    def delete_task(self, task_id: int) -> bool:
        # TODO: タスク削除
        pass
```

### 期待される動作
```bash
python main.py add "買い物" "牛乳とパンを買う"
python main.py list
python main.py complete 1
python main.py delete 1
```

頑張って実装してみてください！
