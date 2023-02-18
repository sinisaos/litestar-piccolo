from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.serializers import create_pydantic_model

# user models
UserModelRegister = create_pydantic_model(
    table=BaseUser,
    include_columns=(
        BaseUser.username,
        BaseUser.email,
        BaseUser.password,
    ),
    model_name="UserModelRegister",
)
UserModelLogin = create_pydantic_model(
    table=BaseUser,
    include_columns=(
        BaseUser.username,
        BaseUser.password,
    ),
    model_name="UserModelLogin",
)
