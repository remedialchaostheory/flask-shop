from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            username = 'Test User'
            password = 'Test Password'
            user = UserModel(username, password)

            self.assertIsNone(UserModel.find_by_username(username))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username(username))
            self.assertIsNotNone(UserModel.find_by_id(1))
