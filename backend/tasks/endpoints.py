import typing as t

from starlite import Request
from starlite.controller import Controller
from starlite.exceptions import NotFoundException
from starlite.handlers import delete, get, patch, post

from accounts.utils import current_user, current_user_guard
from tasks.schema import TaskModelIn, TaskModelOut
from tasks.tables import Task


class TaskController(Controller):
    path = "/api"
    tags = ["Task"]

    @get("/tasks")
    async def tasks(self) -> t.List[TaskModelOut]:
        tasks = await Task.select(
            Task.all_columns(),
            Task.get_readable(),
        ).order_by(Task.id, ascending=False)
        return tasks

    @get("/tasks/{task_id:int}")
    async def single_task(self, task_id: int) -> TaskModelOut:
        task = await Task.objects().get(Task.id == task_id)
        return task.to_dict()

    @post("/tasks", guards=[current_user_guard])
    async def create_task(
        self, data: TaskModelIn, request: Request
    ) -> TaskModelOut:
        session_user = await current_user(request)
        data_map = data.dict()
        data_map["task_user"] = session_user["user"]["id"]
        task = Task(**data_map)
        await task.save()
        return task.to_dict()

    @patch("/tasks/{task_id:int}", guards=[current_user_guard])
    async def update_task(
        self, task_id: int, data: TaskModelIn, request: Request
    ) -> TaskModelOut:
        session_user = await current_user(request)
        task = await Task.objects().get(Task.id == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        for key, value in data.dict().items():
            task.id = task_id
            task.task_user = session_user["user"]["id"]
            setattr(task, key, value)

        await task.save()
        return task.to_dict()

    @delete("/tasks/{task_id:int}", guards=[current_user_guard])
    async def delete_task(self, task_id: int) -> None:
        task = await Task.objects().get(Task.id == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        await task.remove()
