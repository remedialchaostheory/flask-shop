from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_uer(self):
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
        pass

    def test_register_duplicate_user(self):
        pass
