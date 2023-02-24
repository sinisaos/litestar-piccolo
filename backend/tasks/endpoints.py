import typing as t

from starlite import Request
from starlite.controller import Controller
from starlite.exceptions import NotFoundException
from starlite.handlers import delete, get, patch, post

from accounts.guards import current_user, current_user_guard
from tasks.schema import TaskModelIn, TaskModelOut
from tasks.tables import Task
from utils.pagination import Pagination


class TaskController(Controller):
    path = "/api"
    tags = ["Task"]

    @get("/tasks")
    async def tasks(
        self,
        request: Request,
        page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> t.Dict[str, t.Any]:
        paginator = Pagination(page=page, page_size=page_size)
        tasks = await paginator.get_rows(Task, request)
        return {
            "tasks": tasks,
            "total": await paginator.total_pages(Task),
            "page": 1 if page is None else page,
            "page_size": 15 if page_size is None else page_size,
        }

    @get("/tasks/{task_id:int}")
    async def single_task(self, task_id: int) -> TaskModelOut:
        task = (
            await Task.select()
            .where(Task._meta.primary_key == task_id)
            .first()
        )
        return task

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
        task = await Task.objects().get(Task._meta.primary_key == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        for key, value in data.dict().items():
            task.task_user = session_user["user"]["id"]
            setattr(task, key, value)

        await task.save()
        return task.to_dict()

    @delete("/tasks/{task_id:int}", guards=[current_user_guard])
    async def delete_task(self, task_id: int) -> None:
        task = await Task.objects().get(Task._meta.primary_key == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        await task.remove()
