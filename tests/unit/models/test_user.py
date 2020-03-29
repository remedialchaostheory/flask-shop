from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        username = 'Test User'
        password = 'Test Password'
        user = UserModel(username, password)
        self.assertEqual(
            user.username, username, f'Username does not match "{username}"'
        )
        self.assertEqual(
            user.password, password, f'Password does not match "{password}"'
        )
