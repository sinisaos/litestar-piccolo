# Testing

Set a test database in ``piccolo_conf_test.py``.

```python
from piccolo.engine.postgres import PostgresEngine

from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

DB = PostgresEngine(
    config={
        "database": TEST_DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
)
```
Running tests from ``backend`` directory.

```bash
piccolo tester run
```