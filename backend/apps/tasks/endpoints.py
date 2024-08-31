import typing as t

from litestar import Request
from litestar.controller import Controller
from litestar.handlers import delete, get, patch, post

from apps.accounts.guards import current_user, current_user_guard
from apps.tasks.schemas import TaskModelIn, TaskModelOut
from apps.tasks.services import task_service
from apps.tasks.tables import Task
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
        return await task_service.task_single(task_id=task_id)

    @post("/tasks", guards=[current_user_guard])
    async def create_task(
        self, data: TaskModelIn, request: Request
    ) -> TaskModelOut:
        session_user = await current_user(request)
        return await task_service.task_create(
            data=data, session_user=session_user
        )

    @patch("/tasks/{task_id:int}", guards=[current_user_guard])
    async def update_task(
        self, task_id: int, data: TaskModelIn, request: Request
    ) -> TaskModelOut:
        session_user = await current_user(request)
        return await task_service.task_update(
            task_id=task_id, data=data, session_user=session_user
        )

    @delete("/tasks/{task_id:int}", guards=[current_user_guard])
    async def delete_task(self, task_id: int) -> None:
        await task_service.task_delete(task_id=task_id)
