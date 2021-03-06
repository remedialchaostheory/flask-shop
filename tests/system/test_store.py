from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                resp = client.post(f'/store/{store_name}')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name(store_name))
                self.assertDictEqual({
                    'id': 1,
                    'name': store_name,
                    'items': []
                }, json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                client.post(f'/store/{store_name}')
                resp = client.post(f'/store/{store_name}')

                self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                resp = client.delete('/store/Test Store')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(resp.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                StoreModel(store_name).save_to_db()
                resp = client.get(f'/store/{store_name}')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({
                    'id': 1,
                    'name': store_name,
                    'items': []
                }, json.loads(resp.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                resp = client.get(f'/store/{store_name}')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({
                    'message': 'Store not found',
                }, json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                StoreModel(store_name).save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()
                resp = client.get(f'/store/{store_name}')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({
                    'id':
                    1,
                    'name':
                    store_name,
                    'items': [{
                        'name': 'test item',
                        'price': 99.99,
                    }]
                }, json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                StoreModel(store_name).save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual({
                    'stores': [{
                        'id': 1,
                        'name': store_name,
                        'items': []
                    }]
                }, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'Test Store'
                StoreModel(store_name).save_to_db()
                ItemModel('test item', 99.99, 1).save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual({
                    'stores':
                    [{
                        'id': 1,
                        'name': store_name,
                        'items': [{
                            'name': 'test item',
                            'price': 99.99,
                        }]
                    }]
                }, json.loads(resp.data))
