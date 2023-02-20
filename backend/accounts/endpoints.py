import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase
from starlite import Request
from starlite.controller import Controller
from starlite.datastructures import Cookie
from starlite.handlers import delete, get, post
from starlite.response import Response
from starlite.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from accounts.schema import UserModelLogin, UserModelRegister
from accounts.utils import current_user, current_user_guard
from tasks.schema import TaskModelOut
from tasks.tables import Task


class AuthController(Controller):
    path = "/accounts"
    tags = ["Accounts"]

    @post("/register")
    async def register(self, data: UserModelRegister) -> t.Dict[str, str]:
        """
        Register user
        """
        payload = data.dict()
        if (
            await BaseUser.exists()
            .where(BaseUser.email == payload["email"])
            .run()
            or await BaseUser.exists()
            .where(BaseUser.username == payload["username"])
            .run()
        ):
            user_error = "User with that email or username already exists."
            return {"error": user_error}
        # save user
        query = BaseUser(**payload)
        await query.save().run()
        return {"message": "User created"}

    @post("/login")
    async def login(self, data: UserModelLogin) -> Response:
        """
        Login and authenticate user
        """
        payload = data.dict()
        # login user in
        valid_user = await BaseUser.login(
            username=payload["username"], password=payload["password"]
        )
        if not valid_user:
            user_error = "Invalid username or password"
            return {"error": user_error}
        # create session
        session = await SessionsBase.create_session(user_id=valid_user)
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

    @post("/logout", guards=[current_user_guard])
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
        tasks = (
            await Task.select()
            .where(Task.task_user == session_user["user"]["id"])
            .order_by(Task.id, ascending=False)
            .run()
        )
        return tasks

    @delete("/delete", guards=[current_user_guard])
    async def delete_user(self, request: Request) -> None:
        """
        Delete user
        """
        session_user = await current_user(request)
        await BaseUser.delete().where(
            BaseUser.id == session_user["user"]["id"]
        ).run()

        response = Response(
            content=None,
            status_code=HTTP_204_NO_CONTENT,
        )
        response.delete_cookie(key="id")
        return response
