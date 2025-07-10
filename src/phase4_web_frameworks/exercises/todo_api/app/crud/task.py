from sqlalchemy.orm import Session

from ..schemas.task import Priority, TaskCreate
from ..models.task import Task


def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    """タスクを作成"""
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id,
        priority=task.priority,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
