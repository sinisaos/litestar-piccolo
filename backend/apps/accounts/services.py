import typing as t

from litestar.exceptions import NotAuthorizedException
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase

from apps.accounts.schemas import UserModelLogin, UserModelRegister
from apps.tasks.schemas import TaskModelOut
from apps.tasks.tables import Task


class AuthService:

    async def user_register(self, data: UserModelRegister) -> t.Dict[str, str]:
        payload = data.model_dump()
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

    async def user_login(self, data: UserModelLogin) -> SessionsBase:
        payload = data.model_dump()
        # login user in
        valid_user: t.Any = await BaseUser.login(
            username=payload["username"], password=payload["password"]
        )
        if not valid_user:
            raise NotAuthorizedException("Invalid username or password")
        # create session
        session = await SessionsBase.create_session(user_id=valid_user)
        return session

    async def user_profile_tasks(
        self, session_user: dict
    ) -> t.List[TaskModelOut]:
        return (
            await Task.select()
            .where(Task.task_user == session_user["user"]["id"])
            .order_by(Task._meta.primary_key, ascending=False)
            .run()
        )

    async def user_delete(self, session_user: dict) -> None:
        """
        Delete user
        """
        await BaseUser.delete().where(
            BaseUser.id == session_user["user"]["id"]
        ).run()


auth_service = AuthService()
