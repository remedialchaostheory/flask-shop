from models.item import ItemModel
from models.store import StoreModel
from tests.integration.integration_base_test import IntegrationBaseTest


class ItemTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('Test Store').save_to_db()
            item = ItemModel('Test', 99.99, 1)

            self.assertIsNone(
                ItemModel.find_by_name('Test'),
                f'Found item: {item.name}. Expected None.'
            )
            item.save_to_db()
            self.assertIsNotNone(
                ItemModel.find_by_name('Test'),
                f'Did not find item: {item.name}'
            )
            item.delete_from_db()
            self.assertIsNone(
                ItemModel.find_by_name('Test'),
                f'Found item: {item.name}. Expected None.'
            )

    def test_store_relationship(self):
        with self.app_context():
            store_name = 'Test Store'
            store = StoreModel(store_name)
            item = ItemModel('Test', 99.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, store_name)
