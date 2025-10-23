from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_db, get_current_user
from app.crud import get_tasks_for_user, get_task_by_id, create_some_task, update_some_task, delete_some_task
from app.schemas import TaskOut, TaskCreate
from app.schemas.task import TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut)
def create_task(t: TaskCreate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current
    task = create_some_task(db, user.id, t.title, t.start_dt, t.description, t.end_dt)
    return task


@router.get("", response_model=List[TaskOut])
def list_tasks(current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current
    tasks = get_tasks_for_user(db, user.id)
    return tasks


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current
    task = get_task_by_id(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, t: TaskUpdate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current
    task = get_task_by_id(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = t.model_dump(exclude_none=True)
    start = update_data.get("start_dt", task.start_dt)
    end = update_data.get("end_dt", task.end_dt)
    if end and start and end < start:
        raise HTTPException(status_code=400, detail="Дата окончания не может быть раньше даты начала")
    task = update_some_task(db, task, **update_data)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current
    task = get_task_by_id(db, user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_some_task(db, task)
    return {"msg": "deleted"}
