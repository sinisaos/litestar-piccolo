import typing as t

from piccolo_api.crud.serializers import create_pydantic_model

from tasks.tables import Task

# task models
TaskModelIn: t.Any = create_pydantic_model(
    table=Task,
    exclude_columns=(Task.created_at, Task.task_user),
    model_name="TaskModelIn",
)
TaskModelOut: t.Any = create_pydantic_model(
    table=Task,
    include_default_columns=True,
    model_name="TaskModelOut",
)
