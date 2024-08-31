"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig, table_finder

# from apps.tasks.tables

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="tasks",
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY,
        "piccolo_migrations",
    ),
    table_classes=table_finder(
        modules=["apps.tasks.tables"],
        exclude_imported=True,
    ),
    migration_dependencies=[],
    commands=[],
)
