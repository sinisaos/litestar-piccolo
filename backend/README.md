# Instalation

Clone repository in fresh virtualenv and ``cd backend`` into backend folder.

### Setup
-------------------------------------------------------
Create ``.env`` file in ``backend`` directory.

```bash
DB_NAME=your db name
TEST_DB_NAME=your test db name
DB_USER=your db username
DB_PASSWORD=your db password
DB_HOST=your db host
DB_PORT=your db port
SECRET_KEY=your secret key
```

Setup your db credentials in ``piccolo_conf.py``.

```python
from piccolo.engine.postgres import PostgresEngine

from config.main import settings

DB = PostgresEngine(
    config={
        "database": settings.db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    }
)
```

### Install requirements

```bash
pip install -r requirements/requirements.txt
```

### Migrations

```bash
./scripts/migrations.sh
```

### Create admin user

```bash
./scripts/user.sh
```

### Getting started 

```bash
./scripts/start.sh
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) or visit
API docs [localhost:8000/schema/swagger/](http://localhost:8000/schema/swagger).