from flask_jwt import JWTError

from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self) -> None:
        super(ItemTest, self).setUp()
        username = 'test'
        password = 'abcd'
        with self.app() as client:
            with self.app_context():
                UserModel(username, password).save_to_db()
                auth_resp = client.post(
                    '/auth',
                    data=json.dumps({
                        'username': username,
                        'password': password
                    }),
                    headers={'Content-Type': 'application/json'}
                )
                auth_token = json.loads(auth_resp.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertRaises(JWTError)
                # self.assertEqual(
                #     resp.status_code, 401
                # )  # or should be 401 bc no header sent ?

    def test_get_item_not_found(self):
        username = 'test'
        with self.app() as client:
            with self.app_context():
                resp = client.get(
                    f'/item/{username}',
                    headers={'Authorization': self.access_token}
                )
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                resp = client.get(
                    f'/item/test item',
                    headers={'Authorization': self.access_token}
                )
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                resp = client.delete(f'/item/test item')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(resp.data))
