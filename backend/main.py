import typing as t

from litestar import Litestar, asgi
from piccolo.apps.user.tables import BaseUser
from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from piccolo_api.session_auth.tables import SessionsBase

from apps.accounts.endpoints import AuthController
from apps.tasks.endpoints import TaskController
from apps.tasks.tables import Task
from utils.middleware import cors_config, csrf_config

if t.TYPE_CHECKING:
    from litestar.types import Receive, Scope, Send


# mounting Piccolo Admin
@asgi("/admin/", is_mount=True)
async def admin(
    scope: "Scope", receive: "Receive", send: "Send"  # noqa: F821
) -> None:
    await create_admin(tables=[Task, BaseUser, SessionsBase])(
        scope, receive, send
    )


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


app = Litestar(
    route_handlers=[
        admin,
        AuthController,
        TaskController,
    ],
    cors_config=cors_config,
    csrf_config=csrf_config,
    on_startup=[open_database_connection_pool],
    on_shutdown=[close_database_connection_pool],
)
