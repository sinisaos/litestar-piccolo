from piccolo.engine.postgres import PostgresEngine

from config.base import settings

DB = PostgresEngine(
    config={
        "database": settings.test_db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    }
)
