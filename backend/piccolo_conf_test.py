from piccolo.engine.postgres import PostgresEngine

from settings import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, TEST_DB_NAME

DB = PostgresEngine(
    config={
        "database": TEST_DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
)
