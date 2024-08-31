# Testing

Set a test database in ``piccolo_conf_test.py``.

```python
from piccolo.engine.postgres import PostgresEngine

from config.main import settings

DB = PostgresEngine(
    config={
        "database": settings.test_db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    }
)
```
### Install test requirements

```bash
pip install -r requirements/test-requirements.txt
```

### Running tests from ``backend`` directory.

```bash
./scripts/test.sh
```

### Linting

```bash
./scripts/lint.sh
```