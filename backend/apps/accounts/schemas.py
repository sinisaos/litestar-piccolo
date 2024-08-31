import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.serializers import create_pydantic_model

# user models
UserModelRegister: t.Any = create_pydantic_model(
    table=BaseUser,
    include_columns=(
        BaseUser.username,
        BaseUser.email,
        BaseUser.password,
    ),
    model_name="UserModelRegister",
)
UserModelLogin: t.Any = create_pydantic_model(
    table=BaseUser,
    include_columns=(
        BaseUser.username,
        BaseUser.password,
    ),
    model_name="UserModelLogin",
)
