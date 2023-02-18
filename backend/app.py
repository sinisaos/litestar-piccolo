import typing as t

from piccolo.engine import engine_finder
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin
from starlite import Response, Starlite, asgi
from starlite.types import Receive, Scope, Send

from accounts.endpoints import AuthController
from tasks.endpoints import TaskController
from tasks.tables import Task


# mounting Piccolo Admin
@asgi("/admin/", is_mount=True)
async def admin(scope: "Scope", receive: "Receive", send: "Send") -> None:
    await create_admin(tables=[Task, BaseUser])(scope, receive, send)


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
        AuthController,
        TaskController,
    ],
    on_startup=[open_database_connection_pool],
    on_shutdown=[close_database_connection_pool],
)
