from litestar.exceptions import NotFoundException

from apps.tasks.schemas import TaskModelIn, TaskModelOut
from apps.tasks.tables import Task


class TaskService:

    async def task_single(self, task_id: int) -> TaskModelOut:
        return (
            await Task.select()
            .where(Task._meta.primary_key == task_id)
            .first()
        )

    async def task_create(
        self, data: TaskModelIn, session_user: dict
    ) -> TaskModelOut:
        data_map = data.model_dump()
        data_map["task_user"] = session_user["user"]["id"]
        task = Task(**data_map)
        await task.save()
        return task.to_dict()

    async def task_update(
        self, task_id: int, data: TaskModelIn, session_user: dict
    ) -> TaskModelOut:
        task = await Task.objects().get(Task._meta.primary_key == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        for key, value in data.model_dump().items():
            task.task_user = session_user["user"]["id"]
            setattr(task, key, value)

        await task.save()
        return task.to_dict()

    async def task_delete(self, task_id: int) -> None:
        task = await Task.objects().get(Task._meta.primary_key == task_id)
        if not task:
            raise NotFoundException("Task does not exist")
        await task.remove()


task_service = TaskService()
