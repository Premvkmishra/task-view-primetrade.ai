from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models import Task, TaskStatus
from ...schemas import TaskCreate, TaskOut, TaskUpdate, PaginatedTasks
from ...deps import get_current_user

router = APIRouter()

@router.get("/", response_model=dict)
def list_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    status_filter: Optional[TaskStatus] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
):
    q = db.query(Task)
    if current_user.role.value != "admin":
        q = q.filter(Task.user_id == current_user.id)
    if status_filter is not None:
        q = q.filter(Task.status == status_filter)
    total = q.count()
    tasks = q.order_by(Task.id.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"success": True, "data": {"tasks": [TaskOut.model_validate(t) for t in tasks], "total": total}, "message": "OK"}

@router.get("/{task_id}", response_model=dict)
def get_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.role.value != "admin" and task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"success": True, "data": TaskOut.model_validate(task), "message": "OK"}

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = Task(title=payload.title, description=payload.description, status=payload.status or TaskStatus.pending, user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"success": True, "data": TaskOut.model_validate(task), "message": "Created"}

@router.put("/{task_id}", response_model=dict)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.role.value != "admin" and task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status
    db.commit()
    db.refresh(task)
    return {"success": True, "data": TaskOut.model_validate(task), "message": "Updated"}

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.role.value != "admin" and task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(task)
    db.commit()
    return {"success": True, "data": None, "message": "Deleted"}
