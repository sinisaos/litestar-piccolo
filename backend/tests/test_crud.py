from unittest import TestCase

from piccolo.apps.user.tables import BaseUser
from piccolo.testing.model_builder import ModelBuilder
from piccolo_api.session_auth.tables import SessionsBase
from starlite.testing import TestClient

from app import app
from tasks.tables import Task


class TestCrud(TestCase):
    def setUp(self):
        BaseUser.create_table(if_not_exists=True).run_sync()
        SessionsBase.create_table(if_not_exists=True).run_sync()
        Task.create_table(if_not_exists=True).run_sync()
        ModelBuilder.build_sync(Task)

    def tearDown(self):
        Task.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()
        SessionsBase.alter().drop_table().run_sync()

    def test_get_tasks(self):
        with TestClient(app=app) as client:
            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["tasks"]), 1)

    def test_get_single_tasks(self):
        with TestClient(app=app) as client:
            task = Task.select().run_sync()[0]
            response = client.get(f"/api/tasks/{task['id']}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["id"], task["id"])

    def test_task_crud(self):
        with TestClient(app=app) as client:
            # user registration
            payload = {
                "username": "test",
                "email": "test@test.com",
                "password": "1234",
            }
            response = client.post(
                "/accounts/register",
                json=payload,
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.json(),
                {"message": "User created"},
            )

            # user login
            payload = {
                "username": "test",
                "password": "1234",
            }

            login_response = client.post(
                "/accounts/login",
                json=payload,
            )

            cookies = {"id": login_response.cookies["id"]}

            # perform crud operation on protected routes
            user = BaseUser.select().run_sync()[0]

            payload = {
                "name": "Task 100",
                "completed": False,
                "task_user": user["id"],
            }

            response = client.post(
                "/api/tasks",
                json=payload,
                cookies=cookies,
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["id"], 1)

            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["tasks"]), 2)

            payload = {
                "name": "Task 1001",
                "completed": True,
                "task_user": user["id"],
            }

            response = client.patch(
                "/api/tasks/1",
                json=payload,
                cookies=cookies,
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["name"], "Task 1001")
            self.assertEqual(response.json()["completed"], True)

            response = client.delete(
                "/api/tasks/1",
                cookies=cookies,
            )
            self.assertEqual(response.status_code, 204)

            response = client.get("/api/tasks")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["tasks"]), 1)
