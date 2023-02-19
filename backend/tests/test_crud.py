from unittest import TestCase

from piccolo.apps.user.tables import BaseUser
from piccolo.testing.model_builder import ModelBuilder
from starlite.testing import TestClient

from app import app
from tasks.tables import Task


class TestCrud(TestCase):
    def setUp(self):
        BaseUser.create_table(if_not_exists=True).run_sync()
        Task.create_table(if_not_exists=True).run_sync()
        ModelBuilder.build_sync(Task)

    def tearDown(self):
        Task.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()

    def test_get_tasks(self):
        with TestClient(app=app) as client:
            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 1)

    def test_get_single_tasks(self):
        with TestClient(app=app) as client:
            task = Task.select().run_sync()[0]
            response = client.get(f"/api/tasks/{task['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["id"], task["id"])

    def test_task_crud(self):
        with TestClient(app=app) as client:
            user = BaseUser.select().run_sync()[0]
            payload = {
                "name": "Task 100",
                "completed": False,
                "task_user": user["id"],
            }

            response = client.post(
                "/api/tasks",
                json=payload,
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["id"], 1)

            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 2)

            payload = {
                "name": "Task 1001",
                "completed": True,
                "task_user": user["id"],
            }

            response = client.patch(
                "/api/tasks/1",
                json=payload,
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["name"], "Task 1001")
            self.assertEqual(response.json()["completed"], True)

            response = client.delete(
                "/api/tasks/1",
            )
            self.assertEqual(response.status_code, 204)

            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 1)
