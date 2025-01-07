from datetime import datetime

from pydantic import BaseModel


class TaskModelIn(BaseModel):
    name: str
    completed: bool


class TaskModelOut(BaseModel):
    id: int
    name: str
    completed: bool
    created_at: datetime
    task_user: int
