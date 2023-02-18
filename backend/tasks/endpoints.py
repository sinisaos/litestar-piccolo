import typing as t

from starlite.controller import Controller
from starlite.exceptions import NotFoundException
from starlite.handlers import delete, get, patch, post

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

    @post("/tasks")
    async def create_task(self, data: TaskModelIn) -> TaskModelOut:
        task = Task(**data.dict())
        await task.save()
        return task.to_dict()

    @patch("/tasks/{task_id:int}")
    async def update_task(
        self, task_id: int, data: TaskModelIn
    ) -> TaskModelOut:
        task = await Task.objects().get(Task.id == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        for key, value in data.dict().items():
            task.id = task_id
            setattr(task, key, value)

        await task.save()
        return task.to_dict()

    @delete("/tasks/{task_id:int}")
    async def delete_task(self, task_id: int) -> None:
        task = await Task.objects().get(Task.id == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        await task.remove()
