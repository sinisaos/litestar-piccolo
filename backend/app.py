import typing as t

from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from starlite import (
    MediaType,
    Response,
    Starlite,
    asgi,
    delete,
    get,
    patch,
    post,
)
from starlite.plugins.piccolo_orm import PiccoloORMPlugin
from starlite.contrib.jinja import JinjaTemplateEngine
from starlite.types import Receive, Scope, Send

from accounts.endpoints import AuthController
from tasks.endpoints import home
from tasks.piccolo_app import APP_CONFIG
from tasks.tables import Task


# mounting Piccolo Admin
@asgi("/admin/", is_mount=True)
async def admin(scope: "Scope", receive: "Receive", send: "Send") -> None:
    await create_admin(tables=APP_CONFIG.table_classes)(scope, receive, send)


@get("/tasks", tags=["Task"])
async def tasks() -> t.List[Task]:
    tasks = await Task.select().order_by(Task.id, ascending=False)
    return tasks


@post("/tasks", tags=["Task"])
async def create_task(data: Task) -> Task:
    task = Task(**data.to_dict())
    await task.save()
    return task


@patch("/tasks/{task_id:int}", tags=["Task"])
async def update_task(task_id: int, data: Task) -> Task:
    task = await Task.objects().get(Task.id == task_id)
    if not task:
        return Response(
            content={},
            media_type=MediaType.JSON,
            status_code=404,
        )
    for key, value in data.to_dict().items():
        task.id = task_id
        setattr(task, key, value)

    await task.save()
    return task


@delete("/tasks/{task_id:int}", tags=["Task"])
async def delete_task(task_id: int) -> None:
    task = await Task.objects().get(Task.id == task_id)
    if not task:
        return Response(
            content={},
            media_type=MediaType.JSON,
            status_code=404,
        )
    await task.remove()


async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


app = Starlite(
    route_handlers=[
        admin,
        home,
        tasks,
        create_task,
        update_task,
        delete_task,
        AuthController,
    ],
    plugins=[PiccoloORMPlugin()],
    on_startup=[open_database_connection_pool],
    on_shutdown=[close_database_connection_pool],
)
