from models.store import StoreModel
from tests.integration.integration_base_test import IntegrationBaseTest


class StoreTest(IntegrationBaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Test Store')

        self.assertListEqual(
            store.items.all(), [], 'Store items length was not 0 when created.'
        )
