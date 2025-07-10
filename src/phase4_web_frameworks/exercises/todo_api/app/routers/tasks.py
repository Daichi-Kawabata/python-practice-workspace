from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db_session
from ..models.task import Task
from ..core.dependencies import get_current_active_user
from ..schemas.task import TaskCreate, TaskResponse
from ..models.user import User
from ..crud.task import (
    create_task,
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
