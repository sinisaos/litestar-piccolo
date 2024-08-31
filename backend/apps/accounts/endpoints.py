import typing as t

from litestar import Request
from litestar.controller import Controller
from litestar.datastructures import Cookie
from litestar.handlers import delete, get, post
from litestar.response import Response
from litestar.status_codes import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from apps.accounts.guards import current_user, current_user_guard
from apps.accounts.schemas import UserModelLogin, UserModelRegister
from apps.accounts.services import auth_service
from apps.tasks.schemas import TaskModelOut


class AuthController(Controller):
    path = "/accounts"
    tags = ["Accounts"]

    @post("/register")
    async def register(self, data: UserModelRegister) -> t.Dict[str, str]:
        """
        Register user
        """
        return await auth_service.user_register(data=data)

    @post("/login")
    async def login(self, data: UserModelLogin) -> Response:
        """
        Login and authenticate user
        """
        session = await auth_service.user_login(data=data)
        response = Response(
            content={"message": "Succesfully logged in"},
            status_code=HTTP_201_CREATED,
            cookies=[
                Cookie(
                    key="id",
                    value=f"{session['token']}",
                    max_age=3600,
                    httponly=True,
                )
            ],
        )
        return response

    @post("/logout")
    async def logout(self) -> Response:
        """
        Logout user
        """
        response = Response(
            content={"message": "Succesfully logged out"},
            status_code=HTTP_201_CREATED,
        )
        response.delete_cookie(key="id")
        return response

    @get("/profile", guards=[current_user_guard])
    async def profile(self, request: Request) -> t.Dict[str, t.Any]:
        """
        User profile
        """
        return await current_user(request)

    @get("/profile/tasks", guards=[current_user_guard])
    async def profile_tasks(self, request: Request) -> t.List[TaskModelOut]:
        """
        User tasks
        """
        session_user = await current_user(request)
        return await auth_service.user_profile_tasks(session_user=session_user)

    @delete("/delete", guards=[current_user_guard])
    async def delete_user(self, request: Request) -> None:
        """
        Delete user
        """
        session_user = await current_user(request)
        await auth_service.user_delete(session_user=session_user)

        response = Response(
            content=None,
            status_code=HTTP_204_NO_CONTENT,
        )
        response.delete_cookie(key="id")
