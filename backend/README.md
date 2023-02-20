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

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DB = PostgresEngine(
    config={
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
)
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Migrations

```bash
piccolo migrations forwards session_auth
piccolo migrations forwards user
piccolo migrations forwards tasks
```

### Create admin user

```bash
piccolo user create
```

### Getting started 

```bash
python main.py
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) or visit
API docs [localhost:8000/schema/swagger/](http://localhost:8000/schema/swagger).