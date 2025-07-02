from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """タスクを表すデータクラス"""
    
    id: str
    title: str
    description: str
    created_at: date
    completed_at: date | None