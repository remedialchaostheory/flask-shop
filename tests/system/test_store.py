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
        pass

    def test_store_not_found(self):
        pass

    def test_store_not_found_with_items(self):
        pass

    def test_store_list(self):
        pass

    def test_store_list_with_items(self):
        pass
