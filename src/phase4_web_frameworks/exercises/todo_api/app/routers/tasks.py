from fastapi import APIRouter, Depends, HTTPException, status
from flask import g
from sqlalchemy.orm import Session

from ..database import get_db_session
from ..models.task import Task
from ..core.dependencies import get_current_active_user
from ..schemas.task import TaskCreate, TaskResponse
from ..models.user import User
from ..crud.task import (
    get_task_by_id,
    create_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def crate_new_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
) -> Task:
    """新しいタスクを作成する"""
    return create_task(db=db, task=task, user_id=current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """タスクを削除する"""
    success = delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None
