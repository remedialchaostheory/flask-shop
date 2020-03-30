from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post(
                    '/register', data={
                        'username': 'test',
                        'password': 'abcd'
                    }
                )

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(resp.data))

    def test_register_and_login(self):
        username = 'test username'
        password = 'test password'
        with self.app() as client:
            with self.app_context():
                resp = client.post(
                    '/register',
                    data={
                        'username': username,
                        'password': password
                    }
                )
                auth_req = client.post(
                    '/auth',
                    data=json.dumps({
                        'username': username,
                        'password': password
                    }),
                    headers={'Content-Type': 'application/json'}
                )
                self.assertIn('access_token', json.loads(auth_req.data).keys())
