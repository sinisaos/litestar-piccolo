from piccolo.apps.user.tables import BaseUser
from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from starlite import CORSConfig, Starlite, asgi

from accounts.endpoints import AuthController
from tasks.endpoints import TaskController
from tasks.tables import Task


# mounting Piccolo Admin
@asgi("/admin/", is_mount=True)
async def admin(
    scope: "Scope", receive: "Receive", send: "Send"  # noqa: F821
) -> None:
    await create_admin(tables=[Task, BaseUser])(scope, receive, send)


# CORS
cors_config = CORSConfig(
    allow_origins=["http://localhost:8080"],
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    ],
    allow_headers=["Origin", "Content-Type"],
    allow_credentials=True,
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


app = Starlite(
    route_handlers=[
        admin,
        AuthController,
        TaskController,
    ],
    cors_config=cors_config,
    on_startup=[open_database_connection_pool],
    on_shutdown=[close_database_connection_pool],
)
