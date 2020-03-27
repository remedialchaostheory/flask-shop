from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store_name = 'Test Store'
        store = StoreModel(store_name)

        self.assertEqual(
            store.name, store_name,
            f'The name of the store after creation does not equal {store_name}'
        )
