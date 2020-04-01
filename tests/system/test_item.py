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
                self.assertEqual(resp.status_code, 401)

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

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                resp = client.post(
                    f'/item/test item', data={
                        'price': 99.99,
                        'store_id': 1
                    }
                )
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({
                    'name': 'test item',
                    'price': 99.99
                }, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                resp = client.post(
                    f'/item/test item', data={
                        'price': 99.99,
                        'store_id': 1
                    }
                )
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({
                    'message':
                    'An item with name \'test item\' already exists.'
                }, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                resp = client.put(
                    f'/item/test item', data={
                        'price': 99.99,
                        'store_id': 1
                    }
                )
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(
                    ItemModel.find_by_name('test item').price, 99.99
                )
                self.assertDictEqual({
                    'name': 'test item',
                    'price': 99.99
                }, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                self.assertEqual(
                    ItemModel.find_by_name('test item').price, 99.99
                )
                resp = client.put(
                    f'/item/test item', data={
                        'price': 11.00,
                        'store_id': 1
                    }
                )
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(
                    ItemModel.find_by_name('test item').price, 11.00
                )
                self.assertDictEqual({
                    'name': 'test item',
                    'price': 11.00
                }, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({
                    'items': [{
                        'name': 'test item',
                        'price': 99.99
                    }]
                }, json.loads(resp.data))
