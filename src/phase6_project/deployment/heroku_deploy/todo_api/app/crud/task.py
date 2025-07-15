from sqlalchemy.orm import Session

from ..schemas.task import Priority, TaskCreate, TaskUpdate
from ..models.task import Task


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task | None:
    """IDでタスクを取得"""
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


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


def update_task(db: Session, task_id: int, user_id: int, task_data: TaskUpdate) -> Task | None:
    """タスクを更新"""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """タスクを削除"""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True
