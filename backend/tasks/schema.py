from piccolo_api.crud.serializers import create_pydantic_model

from tasks.tables import Task

# task models
TaskModelIn = create_pydantic_model(
    table=Task,
    exclude_columns=(Task.created_at,),
    model_name="TaskModelIn",
)
TaskModelOut = create_pydantic_model(
    table=Task,
    include_default_columns=True,
    model_name="TaskModelOut",
)
