from models.item import ItemModel
from models.store import StoreModel
from tests.integration.integration_base_test import IntegrationBaseTest


class StoreTest(IntegrationBaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Test Store')

        self.assertListEqual(
            store.items.all(), [], 'Store items length was not 0 when created.'
        )

    def test_crud(self):
        with self.app_context():
            store_name = 'Test Store'
            store = StoreModel(store_name)

            self.assertIsNone(
                StoreModel.find_by_name(store_name),
                'Store model should be empty upon creation'
            )
            store.save_to_db()
            self.assertIsNotNone(
                StoreModel.find_by_name(store_name),
                f'Did not find {store_name}'
            )
            store.delete_from_db()
            self.assertIsNone(
                StoreModel.find_by_name(store_name),
                f'The store named "{store_name}" is still present when it should have been deleted'
            )

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item_name = 'Test Item'
            item = ItemModel(item_name, 99.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, item_name)
