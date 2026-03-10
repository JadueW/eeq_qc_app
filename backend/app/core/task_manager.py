from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.db.models import Task


class TaskManager:
    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor(max_workers=settings.max_workers)

    def submit(self, task_id: str, func, *args, **kwargs):
        self.executor.submit(func, task_id, *args, **kwargs)


task_manager = TaskManager()


def update_task(
    db: Session,
    task_id: str,
    *,
    status: str | None = None,
    progress: int | None = None,
    message: str | None = None,
    result_json: str | None = None,
    error_message: str | None = None,
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return
    if status is not None:
        task.status = status
    if progress is not None:
        task.progress = progress
    if message is not None:
        task.message = message
    if result_json is not None:
        task.result_json = result_json
    if error_message is not None:
        task.error_message = error_message
    if status == "running" and task.started_at is None:
        task.started_at = datetime.now()
    if status in {"done", "error"}:
        task.finished_at = datetime.now()
    db.commit()