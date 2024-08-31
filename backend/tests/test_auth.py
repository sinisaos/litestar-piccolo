from unittest import TestCase

from litestar.testing import TestClient
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase

from main import app


class TestAuth(TestCase):
    def setUp(self):
        BaseUser.create_table(if_not_exists=True).run_sync()
        SessionsBase.create_table(if_not_exists=True).run_sync()

    def tearDown(self):
        BaseUser.alter().drop_table().run_sync()
        SessionsBase.alter().drop_table().run_sync()

    def test_auth(self):
        with TestClient(app=app) as client:
            # user registration
            payload = {
                "username": "user",
                "email": "user@user.com",
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

            payload = {
                "username": "user",
                "email": "user@user.com",
                "password": "1234",
            }
            response = client.post(
                "/accounts/register",
                json=payload,
            )
            self.assertEqual(
                response.json(),
                {
                    "error": (
                        "User with that email or username already exists."
                    ),
                },
            )

            # user login
            payload = {
                "username": "user",
                "password": "1234",
            }

            response = client.post(
                "/accounts/login",
                json=payload,
            )

            self.assertEqual(
                response.headers["Set-Cookie"],
                f"id={response.cookies['id']}; HttpOnly; Max-Age=3600; "
                "Path=/; SameSite=lax",
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.json(), {"message": "Succesfully logged in"}
            )

            # user login failed
            payload = {
                "username": "wronguser",
                "password": "wronguser1234",
            }

            response = client.post(
                "/accounts/login",
                json=payload,
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                response.json(),
                {"status_code": 401, "detail": "Invalid username or password"},
            )

            # user logout
            response = client.post(
                "/accounts/logout",
            )
            self.assertEqual(len(response.cookies), 0)
            self.assertEqual(
                response.json(), {"message": "Succesfully logged out"}
            )
            self.assertEqual(response.status_code, 201)

            # user delete
            payload = {
                "username": "user",
                "password": "1234",
            }

            response = client.post(
                "/accounts/login",
                json=payload,
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.json(), {"message": "Succesfully logged in"}
            )

            response = client.get(
                "/accounts/profile",
            )
            self.assertEqual(response.status_code, 200)

            response_delete = client.delete(
                "/accounts/delete",
            )
            self.assertEqual(response_delete.status_code, 204)
