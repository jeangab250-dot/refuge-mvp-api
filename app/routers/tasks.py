
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .. import models, schemas
from ..security import get_db, get_current_user
from ..notifications import send_sms, send_whatsapp

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[schemas.Task])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user), status: str | None = None):
    q = db.query(models.Task).order_by(models.Task.due_at.is_(None), models.Task.due_at.asc())
    if status == "todo":
        q = q.filter(models.Task.is_done == False)  # noqa: E712
    if status == "done":
        q = q.filter(models.Task.is_done == True)   # noqa: E712
    return q.all()

@router.post("", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, background: BackgroundTasks, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_task = models.Task(**task.model_dump(exclude={"send_sms", "send_whatsapp"}))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Notifications immédiates (MVP)
    to_phone = None
    if db_task.assigned_to_user_id:
        assigned = db.get(models.User, db_task.assigned_to_user_id)
        to_phone = assigned.phone if assigned else None

    if to_phone:
        body = f"Tâche: {db_task.title} — échéance: {db_task.due_at}"
        if task.send_sms:
            background.add_task(send_sms, to_phone, body)
        if task.send_whatsapp:
            background.add_task(send_whatsapp, to_phone, body)

    return db_task

@router.post("/{task_id}/complete", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = db.get(models.Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    t.is_done = True
    db.commit()
    db.refresh(t)
    return t
